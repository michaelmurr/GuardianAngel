from app.repositories.valkey import get_valkey
from app.types.general import UserRealtimeData


def get_live_user_data_key(user_id: str, device_id: str) -> str:
    return f"user:{user_id}:device:{device_id}:live_data"


def publish_live_user_data(
    user_id: str, device_id: str, message: UserRealtimeData
) -> None:
    key = get_live_user_data_key(user_id, device_id)
    get_valkey().publish(key, message.model_dump_json())
