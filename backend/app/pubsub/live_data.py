from app.repositories.valkey import get_valkey
from app.types.general import UserRealtimeData


def get_live_user_data_key(user_id: str) -> str:
    return f"user:{user_id}:live_data"


def publish_live_user_data(user_id: str, data: UserRealtimeData) -> None:
    get_valkey().publish(get_live_user_data_key(user_id), data)
