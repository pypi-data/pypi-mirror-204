from pydantic import BaseModel


class ResetPasswordRequest(BaseModel):
    UserPoolId: str
    Username: str
    Password: str
    Permanent: bool
