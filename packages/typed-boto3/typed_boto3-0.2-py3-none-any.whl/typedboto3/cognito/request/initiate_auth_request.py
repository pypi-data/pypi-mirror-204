from typing import Dict, Optional

from pydantic import BaseModel

from typedboto3.cognito.cognito_enum import AuthFlow
from typedboto3.cognito.common import AnalyticsMetadata, UserContextData


class InitiateAuthRequest(BaseModel):
    AuthFlow: AuthFlow
    AuthParameters: Optional[Dict[str, str]]
    ClientMetadata: Optional[Dict[str, str]]
    ClientId: str
    AnalyticsMetadata: Optional[AnalyticsMetadata]
    UserContextData: Optional[UserContextData]
