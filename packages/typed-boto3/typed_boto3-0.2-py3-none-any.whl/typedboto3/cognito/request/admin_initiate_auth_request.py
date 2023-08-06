from typing import Dict, Optional

from pydantic import BaseModel

from typedboto3.cognito.cognito_enum import AuthFlow
from typedboto3.cognito.common import AnalyticsMetadata


class AdminInitiateAuthRequest(BaseModel):
    UserPoolId: str
    ClientId: str
    AuthFlow: AuthFlow
    AuthParameters: Optional[Dict[str, str]]
    ClientMetadata: Optional[Dict[str, str]]
    AnalyticsMetadata: Optional[AnalyticsMetadata]
