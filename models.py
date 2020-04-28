from typing import List

from pydantic import BaseModel


class Alert(BaseModel):
    annotations: dict
    endsAt: str
    generatorURL: str
    labels: dict
    startsAt: str
    status: str


class Event(BaseModel):
    alerts: List[Alert] = None
    commonAnnotations: dict = None
    commonLabels: dict = None
    externalURL: str
    groupKey: str
    groupLabels: dict = None
    receiver: str
    status: str
    version: str
