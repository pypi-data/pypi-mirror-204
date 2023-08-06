from pydantic import BaseModel


class UserAttribute(BaseModel):
    Name: str
    Value: str
