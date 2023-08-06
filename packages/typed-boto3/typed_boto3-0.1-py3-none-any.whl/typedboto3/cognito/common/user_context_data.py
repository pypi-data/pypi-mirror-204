from pydantic import BaseModel


class UserContextData(BaseModel):
    IpAddress: str
    EncodedData: str
