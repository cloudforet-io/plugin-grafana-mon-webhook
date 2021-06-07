from schematics.models import Model
from schematics.types import DictType, StringType

__all__ = ['EventModel']


class EventModel(Model):
    title = StringType(required=True)
    description = StringType(required=True)
    severity = StringType(StringType, required=True, choices=['CRITICAL','ERROR','WARNING','INFO','NOT_AVAILABLE'])
    resource_type = StringType()
    ip_address = StringType()
    rule = StringType(required=True)
    tags = DictType(StringType())