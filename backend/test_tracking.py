import time

import valkey
from app.repositories.valkey import get_valkey

_vk_client: valkey.client.Valkey = get_valkey()

_vk_client.publish(
    "tracking_tasks",
    '{"uid": "user_2xTGnCK2HjOOvj41oUiSxinRXcW","device_id": "YOUR_DEVICE_ID", "action": "START", "destination": {"longitude": 123.5, "latitude": 70.3}}',
)
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )

# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.09702, "latitude": 49.00420}}',
# )
# time.sleep(1)
# _vk_client.publish(
#     "123",
#     '{"battery": 100, "speed": 20.3, "location": {"longitude": 12.097622408462362, "latitude": 49.0040969323266}}',
# )



time.sleep(60)
time.sleep(1)
_vk_client.publish(
    "tracking_tasks",
    '{"uid": "123", "action": "STOP"}',
)
