import valkey
from data import Location
from settings import env


class UserLocationManager:
    USER_DEVICES_KEY = 'users:devices_location'


    def __init__(self):
        self.r = valkey.from_url(env.REDDIS_URL)
    
    def add_or_update_user_device_location(self, uid: str, location: Location, device_id: str):
        self.r.geoadd(self.USER_DEVICES_KEY, [location.latitude, location.longitude, f'{uid}:{device_id}'])

    def search_nearby_user_devices(self, location: Location, radius: int = 30, unit = "m"):
        res = self.r.geosearch(
            self.USER_DEVICES_KEY,
            longitude=location.longitude,
            latitude=location.latitude,
            radius=radius,
            unit=unit,
        )
        print(res)
        return res


manager = UserLocationManager()
# manager.add_or_update_user_device_location('test1', Location(latitude=49.0030835, longitude=12.0962684), 'testdevice1')
# manager.add_or_update_user_device_location('test2', Location(latitude=49.0030833, longitude=12.0962684), 'testdevice2')
# manager.add_or_update_user_device_location('test3', Location(latitude=49.0030834, longitude=12.0962684), 'testdevice3')
# manager.add_or_update_user_device_location('oth', Location(latitude=49.00339400444469, longitude=12.09466249786586), 'oth')
# manager.add_or_update_user_device_location('techbase', Location(latitude=49.00218552608265, longitude=12.100165807298783), 'techbase')
manager.search_nearby_user_devices(Location(latitude=49.00339400444469, longitude=12.09466249786586), radius=1000000, unit='km')

    