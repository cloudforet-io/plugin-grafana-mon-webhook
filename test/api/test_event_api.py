import logging
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json
from pprint import pprint

_LOGGER = logging.getLogger(__name__)


class TestEvent(TestCase):

    def test_parse(self):
        options = {}
        raw_data = {"dashboardId": 10,
                    "evalMatches": [
                        {
                            "metric": "plugin-30d21ef75a5d-bqjgfouoehjujkclb-77c9d6867f-qzmx6",
                            "tags": {
                                "pod": "plugin-30d21ef75a5d-bqjgfouoehjujkclb-77c9d6867f-qzmx6"
                            },
                            "value": 1
                        },
                        {
                            "metric": "plugin-30d21ef75a5d-bqjgfouoehjujkclb-77c9d6867f-znkn8",
                            "tags": {
                                "pod": "plugin-30d21ef75a5d-bqjgfouoehjujkclb-77c9d6867f-znkn8"
                            },
                            "value": 1
                        }
                    ],
                    "imageUrl": "https://grafana.stargate.cloudeco.io/public/img/attachments/LTqROznKoFqum8G0JK7F.png",
                    "message": "[cloudone-dev-v1-eks-cluster] Not Running Pods 0 is OK\n\nFailure level : WorkerNode\nPanel : Not Running Pods 0:OK\nDataSource : Prometheus\nResource : pod\nThreshold : not running pod count > 0 , every 5m , for 5m",
                    "orgId": 1,
                    "panelId": 58,
                    "ruleId": 57,
                    "ruleName": "Not Running Pods 0:OK alert",
                    "ruleUrl": "https://grafana.stargate.cloudeco.io/d/uZaspace/spaceone-dev-cluster-alerts-dashboard?tab=alert&viewPanel=58&orgId=1",
                    "state": "alerting",
                    "tags": {
                    },
                    "title": "[Alerting] Not Running Pods 0:OK alert"
                    }

        parsed_data = self.monitoring.Event.parse({'options': options, 'raw_data': raw_data})
        print_json(parsed_data)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
