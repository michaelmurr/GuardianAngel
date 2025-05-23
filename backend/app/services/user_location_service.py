from app.repositories.valkey import get_valkey
from app.types.general import Location


class UserLocationService:
    PUB_SUB_KEY = "user:locations"

    def __init__(self):
        self.redis = get_valkey()

    
    def _get_uid_device_id_value(self, uid: str, device_id: str):
        return f"{uid}:{device_id}"

    def add_or_update_user_device_location(
        self,
        uid: str,
        device_id: str,
        location: Location,
    ):
        self.redis.geoadd(
            self.PUB_SUB_KEY,
            [
                location.longitude,
                location.latitude,
                self._get_uid_device_id_value(uid, device_id),
            ],
        )

    def search_nearby_user_devices(
        self, location: Location, radius: int = 30, unit="m"
    ):
        res = self.redis.georadius(
            name=self.PUB_SUB_KEY,
            longitude=location.longitude,
            latitude=location.latitude,
            radius=radius,
            unit=unit,
        )
        print(res)
        return res

    def delete_user_device_location(self, uid: str, device_id: str):
        self.redis.zrem(self.PUB_SUB_KEY, self._get_uid_device_id_value(uid, device_id))


USER_LOCATION_SERVICE = UserLocationService()


def get_user_location_service() -> UserLocationService:
    return USER_LOCATION_SERVICE
