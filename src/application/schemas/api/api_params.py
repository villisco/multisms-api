from pydantic import BaseModel, Field

class UrlRequiredParams(BaseModel):
    receiver_groups: str = Field(..., description='Comma separated list of SMS receiving groups. Groups are pre-defined in the config/receiver_groups.yaml file.')