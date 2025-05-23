
import time
import valkey
from settings import env


_vk_client: valkey.client.Valkey = valkey.from_url(env.REDDIS_URL)

_vk_client.publish(
            "tracking_tasks",
            '{"uid": "123", "action": "START", "destination": {"longitude": 123.5, "latitude": 70.3}}',
        )
time.sleep(1)
_vk_client.publish(
            "123",
            '{"battery": 100, "speed": 20.3, "location": {"longitude": 123.5, "latitude": 70.3}}',
        )
time.sleep(1)
_vk_client.publish(
            "tracking_tasks",
            '{"uid": "123", "action": "STOP"}',
        )
