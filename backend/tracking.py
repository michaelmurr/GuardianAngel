import atexit
import json
import threading
import time
from collections import deque
from typing import Deque, Dict, List

import polyline
import valkey
import valkey.client
import valkey.exceptions
from app.pubsub.live_data import get_live_user_data_key
from app.repositories.valkey import get_valkey
from app.types.general import Location, UserRealtimeData
from app.types.tracking import TrackingTaskAction, TrackingTaskMessage
from geopy.distance import geodesic
from pyproj import Transformer
from shapely import Polygon
from shapely.geometry import LineString, Point
from shapely.ops import transform


class GPSSmoother:
    def __init__(self, window_size=3):
        self.points = deque(maxlen=window_size)

    def add_point(self, point):
        self.points.append(point)

    def get_smoothed_point(self):
        if not self.points:
            return None
        avg_lat = sum(p[1] for p in self.points) / len(self.points)
        avg_lng = sum(p[0] for p in self.points) / len(self.points)
        return (avg_lng, avg_lat)


class UserLiveUpdatesSubscriberThread:
    USER_HISTORY_MAX_LEN = 5
    USER_MOVEMENT_THRESHOLD = 5
    UPDATE_SLEEP_INTERVAL = 0.01

    def __init__(self, valkey_client: valkey.Valkey, channel: str):
        self.channel = channel
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._valkey: valkey.Valkey = valkey_client
        self._pubsub: valkey.client.PubSub | None = None
        self._user_history: Deque[UserRealtimeData] = deque(
            maxlen=self.USER_HISTORY_MAX_LEN
        )
        self._corridor: Polygon | None = None
        self._to_m_transformer: Transformer = Transformer.from_crs(
            "EPSG:4326", "EPSG:3857", always_xy=True
        )

    def _calculate_coridor(self, str_polyline: str, buffer_meters: float = 80.0):
        """
        Create a safe coridor based on the user's route polyline

        :param polyline: Geo-polyline
        :param buffer_meters: Width of buffer zone in meters
        :return: True if user is on route, False if off-route
        """

        coords: List[tuple[float, float]] = polyline.decode(str_polyline)

        route = [Location(latitude=lat, longitude=lon) for lat, lon in coords]
        # Convert route to LineString (lon, lat)
        line = LineString([(loc.longitude, loc.latitude) for loc in route])
        # Project to Web Mercator (meters) for accurate buffering
        line_m = transform(self._to_m_transformer.transform, line)
        # Buffer and containment check
        corridor = line_m.buffer(buffer_meters)
        return corridor

    def is_user_in_route_corridor(self, user_location: Location) -> bool:
        """
        Check if user's location is within a buffered corridor of the route.

        :param user_location: Location object (longitude, latitude)
        :return: True if user is on route, False if off-route
        """

        # START Code for projection
        # to_deg = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True).transform

        # line_m = transform(transformer.transform, line)
        # buffer_m = line_m.buffer(buffer_meters)

        # # Transform buffer back to WGS84 (lat/lon)
        # buffer_wgs = transform(to_deg, buffer_m)
        # geojson_dict = buffer_wgs.__geo_interface__
        # import json

        # with open("buffer.geojson", "w") as f:
        #     json.dump(geojson_dict, f)

        # END Code for projection
        point = Point(user_location.longitude, user_location.latitude)
        point_m = transform(self._to_m_transformer.transform, point)
        return self._corridor.contains(point_m)

    def _message_to_user_realtime_data(self, message) -> UserRealtimeData:
        data = json.loads(message["data"].decode("utf-8"))
        return UserRealtimeData(**data)

    def _compare_data(self, new_data: UserRealtimeData):
        if len(self._user_history) >= 2:
            user_in_corridor = self.is_user_in_route_corridor(new_data.location)

            start = self._user_history[0]
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

            # TODO: Implement route deviation logic

    def _proccess_update(self, message):
        new_data = self._message_to_user_realtime_data(message)
        res = self._compare_data(new_data)
        # print(res)
        self._user_history.append(new_data)

    def _redis_subscriber(self):
        try:
            self._pubsub = self._valkey.pubsub(ignore_subscribe_messages=True)
            self._pubsub.subscribe(self.channel)

            # TODO: get the polyline from DB / request
            route_polyline = "_{ajHwnyhAD\\?Np@F~@ANE_@G_@YSc@Gi@CWMe@c@a@qBGeAUw@SuDOaCM_IkBqJmECJa@`GQGDmBLuCN_AFOCcCaA@e@J_AE?I]A@TO@?BcB?"
            self._corridor = self._calculate_coridor(route_polyline)

            while not self._stop_event.is_set():
                try:
                    message = self._pubsub.get_message(timeout=0.1)
                    if message:
                        self._proccess_update(message)

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

        if tracking_task.action == TrackingTaskAction.START:
            # Check if there's an aready running tracking task for this user
            if tracking_task.uid in self._user_updates_subscribers:
                return

            user_updates_subscriber = UserLiveUpdatesSubscriberThread(
                self._vk_client,
                get_live_user_data_key(
                    tracking_task.uid,
                    tracking_task.device_id,
                ),
            )
            user_updates_subscriber.start()
            self._user_updates_subscribers[tracking_task.uid] = user_updates_subscriber

        elif tracking_task.action == TrackingTaskAction.STOP:
            # Check if running tracking task for this user exists
            if tracking_task.uid in self._user_updates_subscribers:
                self._user_updates_subscribers[tracking_task.uid].stop()
                del self._user_updates_subscribers[tracking_task.uid]

    def start(self):
        tracking_pubsub = self._vk_client.pubsub(ignore_subscribe_messages=True)
        self._pubsubs.append(tracking_pubsub)

        tracking_pubsub.subscribe("tracking_tasks")
        while True:
            message = tracking_pubsub.get_message()
            if message:
                self._tracking_handler(message)

            time.sleep(self.UPDATE_SLEEP_INTERVAL)

        # self.r.publish(
        #     "tracking_tasks",
        #     '{"uid": "123", "action": "START", "destination": {"longitude": 123.5, "latitude": 70.3}}',
        # )
        # time.sleep(1)
        # self.r.publish(
        #     "123",
        #     '{"battery": 100, "speed": 20.3, "location": {"longitude": 123.5, "latitude": 70.3}}',
        # )

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
