from pydantic import BaseModel


class EmergencyUserDataDTO(BaseModel):
    uid: str
    device_id: str
