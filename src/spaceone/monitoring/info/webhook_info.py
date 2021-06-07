from spaceone.api.monitoring.plugin import webhook_pb2
from spaceone.core.pygrpc.message_type import *


__all__ = ['PluginInfo']


def PluginInfo(result):
    result['metadata'] = change_struct_type(result['metadata'])
    return webhook_pb2.PluginInfo(**result)
