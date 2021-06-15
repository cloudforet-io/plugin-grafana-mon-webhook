from spaceone.api.monitoring.plugin import event_pb2, event_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Event(BaseAPI, event_pb2_grpc.EventServicer):

    pb2 = event_pb2
    pb2_grpc = event_pb2_grpc

    def parse(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('EventService', metadata) as event_service:
            return self.locator.get_info('EventsInfo', event_service.parse(params))
