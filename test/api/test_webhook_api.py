import logging

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)


class TestWebhook(TestCase):

    def test_init(self):
        v_info = self.monitoring.Webhook.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        self.monitoring.Webhook.verify({'options': {}})