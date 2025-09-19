from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class Receiver(BaseModel):
    number: str = Field(..., description="Phone number")
    name: str = Field(..., description="Phone number owner")

    # validate number format: starts with 5 or 372; max length 11; digits only
    @field_validator("number")
    @classmethod
    def validate_number(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit():
            raise ValueError("Receiver number must contain only digits")
        if not (v.startswith("5") or v.startswith("372")):
            raise ValueError("Receiver number must start with '5' or '372'")
        if len(v) > 11:
            raise ValueError("Receiver number must not be longer than 11 digits")
        return v

class ReceiverGroup(BaseModel):
    # "..." == required
    name: str = Field(..., description='Unique group name')
    description: Optional[str] = Field(None, description="Group description")
    receivers: List[Receiver] = Field(..., min_length=1, max_length=600, description='Each list item is map containing: number,name')

class SMSReceiversConfig(BaseModel):
    receiver_groups: List[ReceiverGroup]