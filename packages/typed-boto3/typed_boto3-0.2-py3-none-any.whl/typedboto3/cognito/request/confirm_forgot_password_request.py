from typing import Dict, Optional

from pydantic import BaseModel
from typedboto3.cognito.common import AnalyticsMetadata, UserContextData


class ConfirmForgotPasswordRequest(BaseModel):
    ClientId: str
    Username: str
    ConfirmationCode: str
    Password: str
    SecretHash: Optional[str]
    AnalyticsMetadata: Optional[AnalyticsMetadata]
    UserContextData: Optional[UserContextData]
    ClientMetadata: Optional[Dict[str, str]]
