from typing import List, Optional

from pydantic import BaseModel
from typedboto3.cognito.cognito_enum import DeliveryMedium
from typedboto3.cognito.common import UserAttribute


class MFAOption(BaseModel):
    DeliveryMedium: DeliveryMedium
    AttributeName: str


class GetCognitoUserResponse(BaseModel):
    Username: str
    UserAttributes: List[UserAttribute]
    MFAOptions: Optional[List[MFAOption]]
    PreferredMfaSetting: Optional[str]
    UserMFASettingList: Optional[List[str]]
