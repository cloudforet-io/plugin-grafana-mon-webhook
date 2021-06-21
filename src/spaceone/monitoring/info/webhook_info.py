__all__ = ['WebhookPluginInfo']

from spaceone.api.monitoring.plugin import webhook_pb2, event_pb2
from spaceone.core.pygrpc.message_type import *


def WebhookPluginInfo(result):
    result['metadata'] = change_struct_type(result['metadata'])
    return webhook_pb2.WebhookPluginInfo(**result)

