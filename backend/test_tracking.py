import datetime
import time

import valkey
from app.pubsub.live_data import get_live_user_data_key
from app.pubsub.tracking_task import get_tracking_tasks_key
from app.repositories.valkey import get_valkey
from app.types.general import Location, UserRealtimeData
from app.types.tracking import TrackingTaskMessage

_vk_client: valkey.client.Valkey = get_valkey()

_vk_client.publish(
    get_tracking_tasks_key(),
    TrackingTaskMessage(
        uid="user_2xTGnCK2HjOOvj41oUiSxinRXcW",
        device_id="YOUR_DEVICE_ID",
        action="START",
        polyline="_{ajHwnyhAD\\?Np@F~@ANE_@G_@YSc@Gi@CWMe@c@a@qBGeAUw@SuDOaCM_IkBqJmECJa@`GQGDmBLuCN_AFOCcCaA@e@J_AE?I]A@TO@?BcB?",
        time_needed=datetime.timedelta(minutes=5),
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00413212316795, longitude=12.097010864806967),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00463886852651, longitude=12.097032322479086),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00510338057528, longitude=12.097064508987264),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00514560872849, longitude=12.098362698150472),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)

time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.005321558981514, longitude=12.097128882003622),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)

time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.005610116050505, longitude=12.097150339675741),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)

time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.005617154006906, longitude=12.09765459497054),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)

time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00563122991673, longitude=12.098105206085043),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00562419196231, longitude=12.098502173019247),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

# Continue

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.006010401962584, longitude=12.097263250349911),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.0065987638244, longitude=12.097497568396879),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00706957188389, longitude=12.097636266774781),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.008099740631096, longitude=12.098521724859875),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)
_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.00864296734731, longitude=12.099750440997589),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.0100794308022, longitude=12.099755516783901),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.010275814260226, longitude=12.099731606958382),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.0107155953031, longitude=12.099813602995022),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.01082282076986, longitude=12.099830584644028),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.01082282076986, longitude=12.099830584644028),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.01082282076986, longitude=12.099830584644028),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.01082282076986, longitude=12.099830584644028),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.01082282076986, longitude=12.099830584644028),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)

_vk_client.publish(
    get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
    UserRealtimeData(
        location=Location(latitude=49.01082282076986, longitude=12.099830584644028),
        battery=100.0,
        speed=20,
    ).model_dump_json(),
)
time.sleep(1)


# _vk_client.publish(
#     get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
#     UserRealtimeData(
#         location=Location(latitude=49.00558196421493, longitude=12.099746718002157),
#         battery=100.0,
#         speed=20,
#     ).model_dump_json(),
# )
# time.sleep(1)

# _vk_client.publish(
#     get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
#     UserRealtimeData(
#         location=Location(latitude=49.00612388425399, longitude=12.099961294723348),
#         battery=100.0,
#         speed=20,
#     ).model_dump_json(),
# )

# time.sleep(1)

# _vk_client.publish(
#     get_live_user_data_key("user_2xTGnCK2HjOOvj41oUiSxinRXcW", "YOUR_DEVICE_ID"),
#     UserRealtimeData(
#         location=Location(latitude=49.006475777225006, longitude=12.100068583083944),
#         battery=100.0,
#         speed=20,
#     ).model_dump_json(),
# )

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
    '{"uid": "123", "action": "STOP", "device_id": "123"}',
)
