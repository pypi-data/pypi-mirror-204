from typing import List, Optional
from pydantic import BaseModel


class HttpHeaders(BaseModel):
    headerName: Optional[str]
    headerValue: Optional[str]


class ContextData(BaseModel):
    IpAddress: str
    ServerName: str
    ServerPath: str
    HttpHeaders: List[HttpHeaders]
    EncodedData: Optional[str]
