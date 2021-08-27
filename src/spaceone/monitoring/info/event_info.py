import functools
from spaceone.core import utils
from spaceone.api.monitoring.plugin import event_pb2
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.core.pygrpc.message_type import *
__all__ = ['EventInfo', 'EventsInfo']


def EventInfo(event_Info_data: EventModel):
    info = {
        'event_key': event_Info_data['event_key'],
        'event_type': event_Info_data['event_type'],
        'description': event_Info_data.get('description'),
        'title': event_Info_data['title'],
        'severity': event_Info_data['severity'],
        'resource': change_struct_type(event_Info_data['resource']),
        'rule': event_Info_data.get('rule'),
        'occurred_at': utils.datetime_to_iso8601(event_Info_data.get('occurred_at')),
        'additional_info': change_struct_type(event_Info_data.get('additional_info'))
    }
    return event_pb2.EventInfo(**info)


def EventsInfo(event_Info_datas, **kwargs):
    return event_pb2.EventsInfo(results=list(map(functools.partial(EventInfo, **kwargs), event_Info_datas)))