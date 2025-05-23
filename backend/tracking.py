import atexit
import json
import threading
import time
from collections import deque
from typing import Deque, Dict, List

import valkey
import valkey.client
from geopy.distance import geodesic
import valkey.exceptions
from settings import env

from app.types.tracking import TrackingTaskMessage, TrackingTaskAction
from app.types.general import UserRealtimeData


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
        self._user_history: Deque[UserRealtimeData] = []


    def _message_to_user_realtime_data(self, message) -> UserRealtimeData:
        data = json.loads(message["data"].decode("utf-8"))
        return UserRealtimeData.model_construct(**data)
    
    
    def _compare_data(self, new_data: UserRealtimeData):
        if len(self._user_history) >= 2:
            start = self._user_history[0]
            end = new_data
            moved_distance = geodesic(
                (start.location.latitude, start.location.longitude),
                (end.location.latitude, end.location.longitude),
            ).meters

            if moved_distance < self.USER_MOVEMENT_THRESHOLD:
                return False
            else:
                return True
            
            #TODO: Implement route deviation logic
            

    def _proccess_update(self, message):
        new_data = self._message_to_user_realtime_data(message)
        res = self._compare_data(new_data)
        print(res)

    def _redis_subscriber(self):
        try:
            self._pubsub = self._valkey.pubsub(ignore_subscribe_messages=True)
            self._pubsub.subscribe(self.channel)

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
            print(f"Thread {threading.current_thread().name} (@{self.channel}): Subscriber stopped.")


    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(
                target=self._redis_subscriber, daemon=True
            )
            self._thread.start()
            print(f"Thread {self._thread.name} (@{self.channel}) started.")

    def stop(self):
        print(f"Stopping thread (@{self.channel}) {threading.current_thread().name}...")
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)  # Wait for the thread to finish
            if self._thread.is_alive():
                print(f"Thread {self._thread.name} (@{self.channel}) did not terminate "
                      "gracefully.")
        else:
            print("Thread was already stopped.")



class Tracker:
    UPDATE_SLEEP_INTERVAL = 0.01

    def __init__(self):
        self._user_updates_subscribers: Dict[str, UserLiveUpdatesSubscriberThread] = {}
        self._pubsubs: List[valkey.client.PubSub] = []
        self._vk_client: valkey.client.Valkey = valkey.from_url(env.REDDIS_URL)


    def _tracking_handler(self, message):
        # get the uid from data and create new thread that watches it
        data = json.loads(message["data"].decode("utf-8"))
        tracking_task = TrackingTaskMessage.model_construct(**data)
        print(tracking_task)

        if tracking_task.action == TrackingTaskAction.START:
            # Check if there's an aready running tracking task for this user
            if tracking_task.uid in self._user_updates_subscribers:
                return
            
            user_updates_subscriber = UserLiveUpdatesSubscriberThread(self._vk_client, tracking_task.uid)
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
