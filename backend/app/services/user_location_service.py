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
    ) -> None:
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

    def get_uids_for_nearby_user_devices_by_uid_and_device(
        self, uid: str, device_id: str, radius: int = 30, unit="m"
    ):
        search_id = self._get_uid_device_id_value(uid, device_id)

        users_devices = self.redis.georadiusbymember(
            name=self.PUB_SUB_KEY,
            member=search_id,
            radius=radius,
            unit=unit,
        )
        results = []
        for ud in users_devices:
            ud = ud.decode("utf-8")
            u = ud.split(":")[0]
            results.append(u)
        results.remove(uid)
        return results

    def delete_user_device_location(self, uid: str, device_id: str):
        self.redis.zrem(self.PUB_SUB_KEY, self._get_uid_device_id_value(uid, device_id))

    def get_location_by_uid_and_device(
        self,
        uid: str,
        device_id: str,
    ) -> Location | None:
        search_id = self._get_uid_device_id_value(uid, device_id)
        res = self.redis.geopos(self.PUB_SUB_KEY, search_id)
        if len(res) > 0:
            return Location(longitude=res[0][0], latitude=res[0][1])
        return


USER_LOCATION_SERVICE = UserLocationService()


def get_user_location_service() -> UserLocationService:
    return USER_LOCATION_SERVICE
