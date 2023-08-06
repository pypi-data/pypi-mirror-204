from typing import Dict, Optional

from pydantic import BaseModel
from typedboto3.cognito.common import AnalyticsMetadata, UserContextData


class ConfirmSignUpRequest(BaseModel):
    ClientId: str
    SecretHash: Optional[str]
    Username: str
    ConfirmationCode: str
    ForceAliasCreation: Optional[bool]
    AnalyticsMetadata: Optional[AnalyticsMetadata]
    UserContextData: Optional[UserContextData]
    ClientMetadata: Optional[Dict[str, str]]
