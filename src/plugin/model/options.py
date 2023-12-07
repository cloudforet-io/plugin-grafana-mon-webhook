from typing import Optional
from pydantic import BaseModel

from spaceone.monitoring.plugin.webhook.model.event.request import EventParseRequest


class Options(BaseModel):
    message_root: Optional[str]

"""
class EventParseOptionsRequest(EventParseRequest):
    options: Optional[Options]
    data: dict
"""