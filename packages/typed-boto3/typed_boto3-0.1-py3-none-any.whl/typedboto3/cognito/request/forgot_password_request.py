from typing import Dict, Optional

from pydantic import BaseModel
from typedboto3.cognito.common import AnalyticsMetadata, UserContextData


class ForgotPasswordRequest(BaseModel):
    ClientId: str
    Username: str
    SecretHash: Optional[str]
    UserContextData: Optional[UserContextData]
    AnalyticsMetadata: Optional[AnalyticsMetadata]
    ClientMetadata: Optional[Dict[str, str]]
