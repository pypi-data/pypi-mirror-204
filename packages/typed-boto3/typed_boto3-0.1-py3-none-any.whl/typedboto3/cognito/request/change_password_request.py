from pydantic import BaseModel


class ChangePasswordRequest(BaseModel):
    PreviousPassword: str
    ProposedPassword: str
    AccessToken: str
