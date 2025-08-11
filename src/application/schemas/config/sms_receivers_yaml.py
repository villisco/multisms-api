from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class ReceiverGroup(BaseModel):
    # "..." == required
    name: str = Field(..., description='Unique group name')
    description: Optional[str] = Field(None, description="Group description")
    receivers: List[int] = Field(..., min_length=1, max_length=600, description='List of phone numbers')

    @field_validator("receivers", mode="before")
    @classmethod
    def validate_each_receiver(cls, value):
        if not isinstance(value, list):
            raise ValueError("Receivers must be a list of integers")

        for number in value:
            number_str = str(number)
            if not number_str.startswith(("5", "372")):
                raise ValueError(f"Receiver number '{number_str}' must start with 5 or 372")

            if len(number_str) > 11:
                raise ValueError(f"Receiver number '{number_str}' must not be longer than 11 digits")

        return value

class SMSReceiversConfig(BaseModel):
    receiver_groups: List[ReceiverGroup]