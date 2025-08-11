from pydantic import BaseModel, Field, ConfigDict
from typing import List

class SmsMessage(BaseModel):
    """
    Example object:
    {
        "flash": False,
        "from": "SMS_SENDER",
        "message": "Hello!",
        "requestReport": False,
        "to": "372561111111"
    }
    """
    # "..." == required
    flash: bool = Field(False, description="Flash short message type on/off (default: False)")
    from_: str = Field(..., alias="from", description="SMS sender")
    message: str = Field(..., description="SMS text")
    requestReport: bool = Field(False, description="Request delivery report on/off")
    to: str = Field(..., description="SMS receiver")

    model_config = ConfigDict(populate_by_name=True) # allows to use `from_` when creating the model

class SmsMessages(BaseModel):
    """
    Example object:
    {
        "messages": []
    }
    """
    messages: List[SmsMessage] = Field(default_factory=list)

    def __len__(self):
        return len(self.messages)