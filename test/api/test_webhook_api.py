import logging

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)


class TestWebHookAWSSNS(TestCase):

    def test_init(self):
        v_info = self.monitroing.Webhook.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.monitroing.Webhook.verify({'options': options})

    def test_parse(self):
        options = {}
        raw_data = {}
        self.monitroing.Event.parse({
            'options': options,
            'raw_data': raw_data
        })