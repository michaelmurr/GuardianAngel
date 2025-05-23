import atexit
import datetime as dt
import json
import threading
import time
from collections import deque
from typing import Deque, Dict, List

import requests
import valkey
import valkey.client
import valkey.exceptions
from app.pubsub.live_data import get_live_user_data_key
from app.pubsub.tracking_task import get_tracking_tasks_key
from app.repositories.valkey import get_valkey
from app.types.general import Location, UserRealtimeData
from app.types.tracking import TrackingTaskAction, TrackingTaskMessage
from geopy.distance import geodesic
from settings import env
from shapely import Polygon
from transformator import GeoTransformator

BACKEND_URL = "google.com"
URL_COMPLETED = f"{BACKEND_URL}/event/completed"
URL_EMERGENCY = f"{BACKEND_URL}/event/emergency/tracking"


class LiveDataRecordManager:
    def __init__(self, records_size=5):
        self._record_data: Deque[UserRealtimeData] = deque(maxlen=records_size)

    def add_record(self, data: UserRealtimeData):
        self._record_data.append(data)

    def get_smoothed_location(self) -> Location:
        if not self._record_data:
            return None
        avg_lng = 0
        avg_lat = 0
        for record in self._record_data:
            avg_lat += record.location.latitude
            avg_lng += record.location.longitude
        ln = len(self._record_data)
        avg_lat /= ln
        avg_lng /= ln
        return Location(longitude=avg_lng, latitude=avg_lat)

    def get_oldest_record(self) -> UserRealtimeData | None:
        if self.get_records_len > 1:
            return self._record_data[0]
        return None

    def get_newest_record(self) -> UserRealtimeData | None:
        if self.get_records_len > 1:
            return self._record_data[-1]
        return None

    def get_records_len(self) -> int:
        return len(self._record_data)


class UserLiveUpdatesSubscriberThread:
    USER_HISTORY_MAX_LEN = 5
    USER_MOVEMENT_THRESHOLD = 5
    UPDATE_SLEEP_INTERVAL = 0.01
    MAX_BUFFER_MINUTES = 15

    def __init__(
        self,
        tracking_data: TrackingTaskMessage,
        valkey_client: valkey.Valkey,
        channel: str,
    ):
        self.channel = channel
        self._polyline: str = tracking_data.polyline
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._valkey: valkey.Valkey = valkey_client
        self._pubsub: valkey.client.PubSub | None = None
        self._live_record_manager: LiveDataRecordManager = LiveDataRecordManager()
        self._corridor: Polygon | None = None
        self._finishing_area: Polygon | None = None
        self._uid = tracking_data.uid
        self._device_id = tracking_data.device_id

        now = dt.datetime.now()
        arrive_by = now + tracking_data.time_needed
        self.max_arrival_time: dt.datetime = arrive_by + dt.timedelta(
            minutes=self.MAX_BUFFER_MINUTES
        )

    def _trigger_emergency(self, reason: str):
        headers = {"X-TRACK-API": env.TRACKING_KEY}
        uuid = get_live_user_data_key(
            self._uid,
            self._device_id,
        )
        requests.post(URL_EMERGENCY, headers=headers, data={"uid": uuid})
        self.stop()

    def _completed_route(self):
        headers = {"X-TRACK-API": env.TRACKING_KEY}
        uuid = get_live_user_data_key(
            self._uid,
            self._device_id,
        )
        requests.post(URL_COMPLETED, headers=headers, data={"uid": uuid})
        self.stop()

    def _is_route_completed(self, avg_loc: Location):
        user_point = GeoTransformator.calculate_point_from_location(avg_loc)
        return self._finishing_area.contains(user_point)

    def _message_to_user_realtime_data(self, message) -> UserRealtimeData:
        data = json.loads(message["data"].decode("utf-8"))
        return UserRealtimeData(**data)

    def _is_moving(self, new_data: UserRealtimeData):
        if len(self._live_record_manager.get_records_len) >= 2:
            start: UserRealtimeData = self._live_record_manager.get_oldest_record
            end = new_data
            print(start.location)
            moved_distance = geodesic(
                (start.location.latitude, start.location.longitude),
                (end.location.latitude, end.location.longitude),
            ).meters

            if moved_distance < self.USER_MOVEMENT_THRESHOLD:
                return False
            else:
                return True

    def _proccess_update(self, message):
        new_data = self._message_to_user_realtime_data(message)
        self._live_record_manager.add_record(new_data)
        avg_loc = self._live_record_manager.get_smoothed_location()

        is_finished = self._is_route_completed(avg_loc)
        if not is_finished:
            is_inside_polygon = GeoTransformator.is_user_in_route_corridor(
                self._corridor, avg_loc
            )
            is_moving = self._is_moving(new_data)

            print(
                new_data,
                "is moving:",
                is_moving,
                " | is inside safe zone:",
                is_inside_polygon,
            )

            if not is_moving:
                self._trigger_emergency("not moving")
            elif not is_inside_polygon:
                self._trigger_emergency("out of polygon")
        else:
            print("finished!")
            self._completed_route()
            return

    def _redis_subscriber(self):
        try:
            self._pubsub = self._valkey.pubsub(ignore_subscribe_messages=True)
            self._pubsub.subscribe(self.channel)

            # TODO: get the polyline from DB / request
            route = GeoTransformator.decode_polyline(self._polyline)
            self._corridor = GeoTransformator.calculate_corridor_from_route(route)
            self._finishing_area = GeoTransformator.calculate_finish_from_location(
                route[-1]
            )

            while not self._stop_event.is_set():
                try:
                    message = self._pubsub.get_message(timeout=0.1)
                    if message:
                        self._proccess_update(message)

                    now = dt.datetime.now()
                    if now > self.max_arrival_time:
                        self._trigger_emergency("time exceeded")

                    time.sleep(self.UPDATE_SLEEP_INTERVAL)

                except valkey.exceptions.ConnectionError as e:
                    print(f"Reconnecting due to connection error: {e}")
                    time.sleep(1)  # Wait before reconnecting
                except Exception as e:
                    print(f"Error processing message: {e}")
                    time.sleep(1)

        except Exception as e:
            print(f"Error in subscriber: {e}")
        finally:
            if self._pubsub:
                self._pubsub.close()
            if self._valkey:
                self._valkey.close()
            print(
                f"Thread {threading.current_thread().name} (@{self.channel}): Subscriber stopped."
            )

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._redis_subscriber, daemon=True)
            self._thread.start()
            print(f"Thread {self._thread.name} (@{self.channel}) started.")

    def stop(self):
        print(f"Stopping thread (@{self.channel}) {threading.current_thread().name}...")
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)  # Wait for the thread to finish
            if self._thread.is_alive():
                print(
                    f"Thread {self._thread.name} (@{self.channel}) did not terminate "
                    "gracefully."
                )
        else:
            print("Thread was already stopped.")


class Tracker:
    UPDATE_SLEEP_INTERVAL = 0.01

    def __init__(self):
        self._user_updates_subscribers: Dict[str, UserLiveUpdatesSubscriberThread] = {}
        self._pubsubs: List[valkey.client.PubSub] = []
        self._vk_client: valkey.client.Valkey = get_valkey()

    def _tracking_handler(self, message):
        # get the uid from data and create new thread that watches it
        data = json.loads(message["data"].decode("utf-8"))
        tracking_task = TrackingTaskMessage.model_construct(**data)
        print(tracking_task)

        user_data_key = get_live_user_data_key(
            tracking_task.uid,
            tracking_task.device_id,
        )

        if tracking_task.action == TrackingTaskAction.START:
            # Check if there's an aready running tracking task for this user
            if tracking_task.uid in self._user_updates_subscribers:
                return

            user_updates_subscriber = UserLiveUpdatesSubscriberThread(
                self._vk_client,
                user_data_key,
                polyline_str=tracking_task.polyline,
                time_needed=tracking_task.time_needed,
            )
            user_updates_subscriber.start()
            self._user_updates_subscribers[user_data_key] = user_updates_subscriber

        elif tracking_task.action == TrackingTaskAction.STOP:
            # Check if running tracking task for this user exists
            if user_data_key in self._user_updates_subscribers:
                self._user_updates_subscribers[tracking_task.uid].stop()
                del self._user_updates_subscribers[tracking_task.uid]

    def ping(self):
        while True:
            print("ping")
            self._vk_client.ping()
            time.sleep(60)

    def start(self):
        tracking_pubsub = self._vk_client.pubsub(ignore_subscribe_messages=True)
        self._pubsubs.append(tracking_pubsub)
        tracking_pubsub.subscribe(get_tracking_tasks_key())

        ping_thread = threading.Thread(target=self.ping, daemon=True)
        ping_thread.start()

        while True:
            try:
                message = tracking_pubsub.get_message()
                if message:
                    self._tracking_handler(message)

                time.sleep(self.UPDATE_SLEEP_INTERVAL)

            except valkey.exceptions.ConnectionError as e:
                print(f"Reconnecting due to connection error in main loop: {e}")
                time.sleep(1)  # Wait before reconnecting
            except Exception as e:
                print(f"Error processing message in main loop: {e}")
                time.sleep(1)

    def exit_handler(self):
        print("Exiting")
        for _, subscriber in self._user_updates_subscribers.items():
            subscriber.stop()

        for pubsub in self._pubsubs:
            pubsub.close()
        print("Proccesses stopped")


if __name__ == "__main__":
    tracker = Tracker()
    atexit.register(tracker.exit_handler)
    tracker.start()
