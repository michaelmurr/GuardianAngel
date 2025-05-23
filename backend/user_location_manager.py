from app.repositories.valkey import get_valkey
from app.types.general import Location


class UserLocationManager:
    USER_DEVICES_KEY = "users:devices_location"

    def __init__(self):
        self.r = get_valkey()

    def _get_uid_device_id_value(uid: str, device_id: str):
        return f"{uid}:{device_id}"

    def add_or_update_user_device_location(
        self, uid: str, location: Location, device_id: str
    ):
        self.r.geoadd(
            self.USER_DEVICES_KEY,
            [
                location.longitude,
                location.latitude,
                self._get_uid_device_id_value(uid, device_id),
            ],
        )

    def search_nearby_user_devices(
        self, location: Location, radius: int = 30, unit="m"
    ):
        res = self.r.georadius(
            name=self.USER_DEVICES_KEY,
            longitude=location.longitude,
            latitude=location.latitude,
            radius=radius,
            unit=unit,
        )
        print(res)
        return res

    def delete_user_device_location(self, uid: str, device_id: str):
        self.r.zrem(
            self.USER_DEVICES_KEY, self._get_uid_device_id_value(uid, device_id)
        )
