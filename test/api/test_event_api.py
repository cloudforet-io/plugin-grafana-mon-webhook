import logging
import unittest
import os
import json
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json
from pprint import pprint

_LOGGER = logging.getLogger(__name__)
TEST_JSON = os.environ.get('test_json', None)

def _get_json():
    with open(TEST_JSON) as json_file:
        json_data = json.load(json_file)
        return json_data

class TestEvent(TestCase):

    def test_parse(self):
        params = _get_json()
        """
        {
            "options": {

            },
            "data": {
                "ruleId": 74.0,
                "orgId": 1.0,
                "ruleName": "API Server Request Latency TEMP",
                "dashboardId": 10.0,
                "message": "Temporary test Webhook\n- API Server Request Latency",
                "imageUrl": "https://grafana.stargate.cloudeco.io/public/img/attachments/qmNDGfjVSyG53lu9RmOb.png",
                "evalMatches": [
                    {
                        "value": 0.48198821648077433,
                        "metric": "{}",
                        "tags": null
                    }
                ],
                "title": "[Alerting] API Server Request Latency TEMP",
                "tags": {
                },
                "panelId": 102.0,
                "state": "alerting",
                "ruleUrl": "https://grafana.stargate.cloudeco.io/d/uZaspace/spaceone-dev-cluster-alerts-dashboard?tab=alert&viewPanel=102&orgId=1"
            }
        }
        """
        parsed_data = self.monitoring.Event.parse({'options': params.get('options'), 'data': params.get('data')})
        print_json(parsed_data)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
