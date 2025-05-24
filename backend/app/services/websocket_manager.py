import asyncio
import json
import time
from typing import Dict, List, Set

from app.pubsub.live_data import get_live_user_data_key
from app.repositories.valkey import get_valkey
from app.types.general import UserRealtimeData
from app.websocket.connection_manager import (
    USERID,
    ConnectionManager,
    get_connection_manager,
)
from app.websocket.outbound_messages import (
    FriendLocationUpdatePayload,
    OutboundFriendLocationUpdateMessage,
)


class WebsocketManager:
    def __init__(self, connection_manager: ConnectionManager):
        self._cm: ConnectionManager = connection_manager
        self._redis = get_valkey()
        self._user_friends: Dict[USERID, Set[USERID]] = {}
        self._tasks: Dict[USERID, asyncio.Task] = {}

        self._data_to_send: Dict[USERID, Set[UserRealtimeData]] = []

        self._cm.set_on_connect_callback(self.on_connect)
        self._cm.set_on_disconnect_callback(self.on_disconnect)

    def on_connect(self, uid: USERID, device_id: str, friend_list: Set[USERID]):
        pubsub = self._redis.pubsub()
        topic = get_live_user_data_key(
            uid,
            device_id,
        )
        pubsub.subscribe(topic)

        self._user_friends[uid] = friend_list
        for friend in friend_list:
            self._user_friends.get(friend).add(uid)

        async def _polling_loop():
            async for message in pubsub.listen():
                data = UserRealtimeData(**json.loads(message["data"].decode("utf-8")))
                await self._dispatch_to_friends(uid, data)

        task = asyncio.create_task(_polling_loop())
        self._tasks[uid] = task

    def _dispatch_to_friends(self, uid: USERID, data: UserRealtimeData):
        fid = self._user_friends.get(uid, None)
        if fid:
            # TODO change the type of sending data
            self._cm.broadcast_message(fid, data)

    def client_disconnect(self, uid: USERID, device_id: str):
        task = self._tasks.pop(uid)
        task.cancel()
        self._user_friends.pop(uid)
        for _, friends in self._user_friends.items():
            friends.remove(uid)

    def start(self):
        while True:
            print("polling", self._tasks)
            for uid in self._tasks:
                payload_list: List[FriendLocationUpdatePayload] = []
                data = self._data_to_send.get(uid)
                for update in data:
                    payload_list.append(FriendLocationUpdatePayload(**update))

                print(payload_list)

                self._cm.send_message(
                    uid, OutboundFriendLocationUpdateMessage(payload=payload_list)
                )
            self._tasks = []
            time.sleep(1)

    async def stop(self):
        for _, task in self._tasks.items():
            task.cancel()


cm = get_connection_manager()
WEBSOCKET_MANAGER = WebsocketManager(cm)


def get_websocket_manager():
    return WEBSOCKET_MANAGER
