from pydantic import BaseModel, RootModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID

from application.schemas.config.sms_receivers_yaml import SMSReceiversConfig

class MetaInfo(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    partial_success: bool = Field(default=False)

class FailureItem(BaseModel):
    code: str
    receiver: str
    message: str

class DataPayload(BaseModel):
    sms_generated_count: int = Field(2, description="Total SMS messages generated")
    sms_sent_count: int = Field(2, description="Total SMS messages sent")
    sms_sent_failed_count: int = Field(0, description="Total SMS failed to be sent")
    failures: Optional[List[FailureItem]] = Field(default_factory=list)

class ApiErrorResponse(BaseModel):
    id: UUID
    error: MetaInfo

class ApiSuccessResponse(BaseModel):
    id: UUID
    meta: MetaInfo
    data: DataPayload

class ApiConfigResponse(RootModel[SMSReceiversConfig]):
    pass

class HealthResponse(BaseModel):
    status: str = Field("up", description="Application healthy")