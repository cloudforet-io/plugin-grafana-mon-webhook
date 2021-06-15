from schematics.models import Model
from schematics.types import DictType, StringType, ModelType, DateType

__all__ = ['EventModel']


class ResourceModel(Model):
    resource_id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    ip_address = StringType(serialize_when_none=False)
    resource_type = StringType(serialize_when_none=False)


class EventModel(Model):
    event_key = StringType(required=True)
    event_type = StringType(choices=['RECOVERY', 'ALERT'], default='ALERT')
    title = StringType(required=True)
    description = StringType(default='')
    severity = StringType(choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'NOT_AVAILABLE'], default='INFO')
    resource = ModelType(ResourceModel)
    rule = StringType(default='')
    occurred_at = DateType()
    tags = DictType(StringType(), default={})


