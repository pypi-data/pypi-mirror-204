from typing import Dict, Optional

from pydantic import BaseModel
from typedboto3.cognito.cognito_enum import Challenge
from typedboto3.cognito.common import DeviceMetadata


class AuthenticationResult(BaseModel):
    AccessToken: str
    ExpiresIn: int
    TokenType: str
    RefreshToken: Optional[str]
    IdToken: str
    NewDeviceMetadata: Optional[DeviceMetadata]


class AdminInitiateAuthResponse(BaseModel):
    ChallengeName: Challenge
    Session: str
    ChallengeParameters: Dict[str, str]
    AuthenticationResult: AuthenticationResult
