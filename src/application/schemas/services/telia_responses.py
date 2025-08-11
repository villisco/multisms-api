from pydantic import BaseModel, Field
from typing import List, Optional

class MessagePart(BaseModel):
    opMessageUid: str
    messageLength: int

class AcceptedMessage(BaseModel):
    to: str
    from_: str = Field(..., alias="from")
    message: str
    requestReport: bool
    flash: bool
    parts: List[MessagePart] = Field(default_factory=list)
    messageFormat: str

class UnacceptableMessage(BaseModel):
    to: str
    from_: str = Field(..., alias="from")
    message: str
    requestReport: bool
    flash: bool
    messageFormat: str
    errorMessage: Optional[str] = None   # or: = ""

class TeliaSuccessResponse(BaseModel):
    allAcceptedSuccessfully: bool
    receivedMessagesCount: int
    acceptedMessagesCount: int
    unacceptableMessagesCount: int
    acceptedMessages: List[AcceptedMessage] = Field(default_factory=list)
    unacceptableMessages: List[UnacceptableMessage] = Field(default_factory=list)

    model_config = dict(
        openapi_extra={
            "description": "Telia POST sms successful response examples",
            "examples": {
                "Partial Success": {
                    "allAcceptedSuccessfully": False,
                    "receivedMessagesCount": 2,
                    "acceptedMessagesCount": 1,  
                    "unacceptableMessagesCount": 1, 
                    "acceptedMessages": [    
                        {       
                            "to": "372xxxxxxx",       
                            "from": "123",       
                            "message": "sms 1",       
                            "requestReport": True,       
                            "flash": False,       
                            "parts": [      
                                {           
                                    "opMessageUid": "<opMessageUid 1>",          
                                    "messageLength": 5        
                                }       
                            ],       
                            "messageFormat": "GSM7" # Supported short message encodings: GSM7 / UCS-2 
                        }   
                    ],   
                    "unacceptableMessages": [  
                        {       
                            "to": "371xxxxxxx",       
                            "from": "123",       
                            "message": "sms 2 õäöü",       
                            "requestReport": True,       
                            "flash": False,       
                            "messageFormat": "UCS-2",      
                            "errorMessage": "Recipient number is not allowed"   
                        }   
                    ] 
                },
                "Success (all messages sent)": {
                    "allAcceptedSuccessfully": True,
                    "receivedMessagesCount": 2, 
                    "acceptedMessagesCount": 2, 
                    "unacceptableMessagesCount": 0,
                    "acceptedMessages": [    
                        {       
                            "to": "372xxxxxxx",       
                            "from": "123",       
                            "message": "sms 1",       
                            "requestReport": True,       
                            "flash": False,       
                            "parts": [         
                                {           
                                    "opMessageUid": "<opMessageUid 11>",           
                                    "messageLength": 5        
                                }       
                            ],       
                            "messageFormat": "GSM7" # Supported short message encodings: GSM7 / UCS-2
                        },
                        {       
                            "to": "371xxxxxxx",       
                            "from": "123",       
                            "message": "sms 2",       
                            "requestReport": True,       
                            "flash": False,      
                            "parts": [        
                                {           
                                    "opMessageUid": "<opMessageUid 12>",          
                                    "messageLength": 5        
                                }       
                            ],   
                            "messageFormat": "GSM7",     
                        }   
                    ],   
                    "unacceptableMessages": [] 
                }
            }
        }
    )