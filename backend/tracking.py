import atexit
import json
from typing import Deque
import valkey
from data import Action, UserRealtimeData, UserWalkControlData
from settings import env
import time
import threading
from valkey.client import PubSub
from geopy.distance import geodesic
from collections import deque


class Tracker: 
    USER_HISTORY_MAX_LEN = 5
    USER_MOVEMENT_THRESHOLD = 5

    threads = {}
    pubsubs = []


    def __init__(self):
        self.r = valkey.from_url(env.REDDIS_URL)


    def compare_data(self, history: Deque[UserRealtimeData], new_data: UserRealtimeData):  
        if len(history) >= 2:
                start = history[0]
                end = new_data
                moved_distance = geodesic((start.location.latitude, start.location.longitude), (end.location.latitude, end.location.longitude)).meters

                if moved_distance < self.USER_MOVEMENT_THRESHOLD:
                    return False
                else:
                    return True
        


    def user_tracking_handler(self, message) -> UserRealtimeData:
        data = json.loads(message['data'].decode('utf-8'))
        realtime_data = UserRealtimeData.model_construct(**data)
        print(realtime_data)
        return realtime_data


    def user_tracking_threading(self, control_data: UserWalkControlData, uidP: PubSub):
        uidP.subscribe(control_data.uid)
        user_history = deque(maxlen=self.USER_HISTORY_MAX_LEN)
        while True:
            message = uidP.get_message()
            if message:
                new_data = self.user_tracking_handler(message)
                print(self.compare_data(user_history, new_data))
                user_history.append(new_data)

            time.sleep(0.01) 


    def tracking_handler(self, message):
        # get the uid from data and create new thread that watches it
        data = json.loads(message['data'].decode('utf-8'))
        control_data = UserWalkControlData.model_construct(**data)
        print(control_data)
        if (control_data.action == Action.START):
            uidP = self.r.pubsub(ignore_subscribe_messages=True)
            self.pubsubs.append(uidP)
            

            thread = threading.Thread(target=self.user_tracking_threading, args=(control_data, uidP))
            self.threads[control_data.uid] = thread
            thread.start()

        elif control_data.action == Action.STOP:
            self.threads[control_data.uid].join(timeout=1.0)


    def start(self):
        p = self.r.pubsub(ignore_subscribe_messages=True)
        self.pubsubs.append(p)

        p.subscribe(**{'tracking_tasks': self.tracking_handler})
        thread = p.run_in_thread(sleep_time=0.01)
        self.threads['tracking_tasks'] = thread

        self.r.publish('tracking_tasks', '{"uid": "123", "action": "START", "destination": {"longitude": 123.5, "latitude": 70.3}}')
        time.sleep(1)
        self.r.publish('123', '{"battery": 100, "speed": 20.3, "location": {"longitude": 123.5, "latitude": 70.3}}')


    def exit_handler(self):
        print('Exiting')
        for _, thread in self.threads.items():
            try:
                thread.stop()
            except: 
                pass
            thread.join(timeout=1.0)

        for pubsub in self.pubsubs:
            pubsub.close()
        print('Proccesses stopped')



if __name__ == "__main__":
    tracker = Tracker()
    atexit.register(tracker.exit_handler)
    tracker.start()
