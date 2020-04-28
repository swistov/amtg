from typing import List

from pydantic import BaseModel


class Alert(BaseModel):
    annotations: dict
    endsAt: str
    generatorURL: str
    labels: dict
    startsAt: str


class Event(BaseModel):
    alerts: List[Alert]
    commonAnnotations: dict = None
    commonLabels: dict = None
    externalURL: str
    groupKey: int
    groupLabels: dict = None
    receiver: str
    status: str
    version: str