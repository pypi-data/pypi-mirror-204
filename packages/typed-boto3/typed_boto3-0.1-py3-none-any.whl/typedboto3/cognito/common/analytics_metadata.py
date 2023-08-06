from typing import Optional
from pydantic import BaseModel


class AnalyticsMetadata(BaseModel):
    AnalyticsEndpointId: Optional[str]
