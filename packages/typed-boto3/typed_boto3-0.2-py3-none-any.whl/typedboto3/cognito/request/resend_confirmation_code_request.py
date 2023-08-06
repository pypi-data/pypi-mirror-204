from typing import Dict, Optional

from pydantic import BaseModel
from typedboto3.cognito.common import AnalyticsMetadata, UserContextData


class ResendConfirmationCodeRequest(BaseModel):
    ClientId: str
    Username: str
    SecretHash: Optional[str]
    UserContextData: Optional[UserContextData]
    AnalyticsMetaData: Optional[AnalyticsMetadata]
    ClientMetadata: Optional[Dict[str, str]]
