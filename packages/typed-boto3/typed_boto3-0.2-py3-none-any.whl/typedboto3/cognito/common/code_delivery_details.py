from pydantic import BaseModel
from typedboto3.cognito.cognito_enum import DeliveryMedium


class CodeDeliveryDetails(BaseModel):
    Destination: str
    DeliveryMedium: DeliveryMedium
    AttributeName: str
