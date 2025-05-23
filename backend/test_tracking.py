import time

import valkey
from app.pubsub.tracking_task import get_tracking_tasks_key
from app.repositories.valkey import get_valkey
from app.types.tracking import TrackingTaskMessage

_vk_client: valkey.client.Valkey = get_valkey()


_vk_client.publish(
    get_tracking_tasks_key(),
    TrackingTaskMessage(
        uid="user_2xTGnCK2HjOOvj41oUiSxinRXcW",
        device_id="YOUR_DEVICE_ID",
        action="START",
        polyline="cgcjHifzhAWC?S?_@?kACoFH@@EBg@QEPcA\\_BNgA?a@LcCDg@Jy@LwD?MUAWA?He@CcAEE]D}HA[?m@XcFiBo@",
    ).model_dump_json(),
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
