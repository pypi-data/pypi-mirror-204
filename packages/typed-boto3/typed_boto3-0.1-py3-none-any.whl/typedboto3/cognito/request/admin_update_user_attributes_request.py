from typing import Dict, List, Optional
from pydantic import BaseModel
from typedboto3.cognito.common import UserAttribute


class AdminUpdateUserAttributesRequest(BaseModel):
    UserPoolId: str
    Username: str
    UserAttributes: List[UserAttribute]
    ClientMetadata: Optional[Dict[str, str]]
