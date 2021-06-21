from spaceone.api.monitoring.plugin import webhook_pb2, webhook_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Webhook(BaseAPI, webhook_pb2_grpc.WebhookServicer):

    pb2 = webhook_pb2
    pb2_grpc = webhook_pb2_grpc

    def init(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('WebhookService', metadata) as webhook_service:
            return self.locator.get_info('WebhookPluginInfo', webhook_service.init(params))

    def verify(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('WebhookService', metadata) as webhook_service:
            webhook_service.verify(params)
            return self.locator.get_info('EmptyInfo')
