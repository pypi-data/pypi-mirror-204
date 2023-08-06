from typing import Optional
from pydantic import BaseModel
from typedboto3.cognito.common import CodeDeliveryDetails


class SignUpResponse(BaseModel):
    UserConfirmed: bool
    CodeDeliveryDetails: Optional[CodeDeliveryDetails]
    UserSub: str
