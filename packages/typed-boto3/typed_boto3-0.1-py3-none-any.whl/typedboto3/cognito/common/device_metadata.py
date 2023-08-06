from pydantic import BaseModel


class DeviceMetadata(BaseModel):
    DeviceKey: str
    DeviceGroupKey: str
