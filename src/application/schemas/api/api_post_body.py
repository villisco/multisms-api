from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime

class PostBodySms(BaseModel):
    receiver_groups: List[str]
    sms_text: str

class AlertAnnotation(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None

class AlertLabel(BaseModel):
    # most used alert labels
    summary: Optional[str] = None
    service: Optional[str] = None
    teenus: Optional[str] = None
    severity: Optional[str] = None

    # allow other unknown labels
    model_config = ConfigDict(extra='allow')

class Alert(BaseModel):
    annotations: AlertAnnotation
    endsAt: datetime
    generatorURL: HttpUrl
    labels: AlertLabel
    startsAt: datetime
    status: str

class AlertmanagerWebhookPayload(BaseModel):
    alerts: List[Alert]
    commonAnnotations: Optional[AlertAnnotation] = None
    commonLabels: Optional[AlertLabel] = None
    externalURL: HttpUrl
    groupKey: str
    groupLabels: Dict[str, str]
    receiver: str
    status: str
    version: str

    model_config = dict(
        openapi_extra={
            "description": "Alertmanager POST data examples",
            "examples": {
                "firing_alert": {
                    "summary": "Firing alert",
                    "description": "Alert sent by Alertmanager",
                    "value": {
                        "version": "4",
                        "groupKey": "...",
                        "status": "firing",
                        "receiver": "my-receiver",
                        "groupLabels": {
                            "alertname": "HighCPUUsage"
                        },
                        "commonLabels": {
                            "alertname": "HighCPUUsage",
                            "severity": "critical"
                        },
                        "commonAnnotations": {
                            "summary": "CPU usage is above 90%"
                        },
                        "externalURL": "https://alertmanager.example.com",
                        "alerts": [
                            {
                                "status": "firing",
                                "labels": {
                                    "alertname": "HighCPUUsage",
                                    "instance": "myserver",
                                    "severity": "critical"
                                },
                                "annotations": {
                                    "summary": "CPU usage is above 90%"
                                },
                                "startsAt": "2025-05-09T08:00:00Z",
                                "endsAt": "0001-01-01T00:00:00Z",
                                "generatorURL": "https://prometheus/graph?g0.expr=..."
                            }
                        ]
                    }
                }
            }
        }
    )