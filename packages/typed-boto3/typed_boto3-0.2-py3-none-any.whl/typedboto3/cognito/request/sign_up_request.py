from typing import Dict, List, Optional
from pydantic import BaseModel
from typedboto3.cognito.common import AnalyticsMetadata, UserAttribute, UserContextData


class SignUpRequest(BaseModel):
    ClientId: str
    Username: str
    Password: str
    SecretHash: Optional[str]
    UserAttributes: Optional[List[UserAttribute]]
    ValidationData: Optional[List[UserAttribute]]
    AnalyticsMetadata: Optional[AnalyticsMetadata]
    UserContextData: Optional[UserContextData]
    ClientMetadata: Optional[Dict[str, str]]
