from pydantic import BaseModel
from typedboto3.cognito.common import CodeDeliveryDetails


class ForgotPasswordResponse(BaseModel):
    CodeDeliveryDetails: CodeDeliveryDetails
