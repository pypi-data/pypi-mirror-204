from typing import Optional

from pydantic import BaseModel


class RevokeTokenRequest(BaseModel):
    Token: str
    ClientId: str
    ClientSecret: Optional[str]
