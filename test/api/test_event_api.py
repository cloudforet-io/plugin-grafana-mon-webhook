import logging
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json
from pprint import pprint

_LOGGER = logging.getLogger(__name__)


class TestEvent(TestCase):

    def test_parse(self):
        options = {}
        params = {
            "options": {},
            "data": {
                "ruleName": "Test notification",
                "title": "[Alerting] Test notification",
                "ruleUrl": "https://grafana.stargate.cloudeco.io/",
                "message": "Someone is testing the alert notification within Grafana.",
                "state": "alerting",
                "dashboardId": 1.0,
                "ruleId": 3.0853793301526e+18,
                "panelId": 1.0,
                "tags": {},
                "evalMatches": [
                    {
                        "metric": "High value",
                        "value": 100.0,
                        "tags": 'null',
                    },
                    {
                        "value": 200.0,
                        "tags": 'null',
                        "metric": "Higher Value"
                    }
                ],
                "orgId": 0.0,
                "imageUrl": "https://grafana.com/assets/img/blog/mixed_styles.png"
            }
        }
        parsed_data = self.monitoring.Event.parse({'options': params.get('options'), 'data': params.get('data')})
        print_json(parsed_data)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
