import logging
import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)
TEST_JSON = os.environ.get('test_json', None)


class TestEvent(TestCase):

    def test_parse(self):
        params1 = {
            "options": {

            },
            "data": {
                "tags": {

                },
                "evalMatches": [

                ],
                "ruleUrl": "https://grafana.stargate.cloudeco.io/d/uZaspace/spaceone-dev-cluster-alerts-dashboard?tab=alert&viewPanel=58&orgId=1",
                "ruleId": 57.0,
                "ruleName": "Not Running Pods 0:OK alert",
                "message": "[cloudone-dev-v1-eks-cluster] Not Running Pods 0 is OK\n\nFailure level : WorkerNode\nPanel : Not Running Pods 0:OK\nDataSource : Prometheus\nResource : pod\nThreshold : not running pod count > 0 , every 5m , for 5m",
                "imageUrl": "https://grafana.stargate.cloudeco.io/public/img/attachments/GjadpyvgFPVwSGtrfeww.png",
                "dashboardId": 10.0,
                "state": "ok",
                "orgId": 1.0,
                "panelId": 58.0,
                "title": "[OK] Not Running Pods 0:OK alert"
            }
        }
        params2 = {
            "options": {

            },
            "data": {
                "evalMatches": [
                    {
                        "tags": {
                            "pod": "plugin-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9"
                        },
                        "metric": "plugin-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9",
                        "value": 0.15384615384615385
                    }
                ],
                "imageUrl": "https://grafana.stargate.cloudeco.io/public/img/attachments/yo4maLzA629Oh24c1g1g.png",
                "ruleId": 57.0,
                "title": "[Alerting] Not Running Pods 0:OK alert",
                "panelId": 58.0,
                "state": "alerting",
                "orgId": 1.0,
                "ruleName": "Not Running Pods 0:OK alert",
                "ruleUrl": "https://grafana.stargate.cloudeco.io/d/uZaspace/spaceone-dev-cluster-alerts-dashboard?tab=alert&viewPanel=58&orgId=1",
                "dashboardId": 10.0,
                "message": "[cloudone-dev-v1-eks-cluster] Not Running Pods 0 is OK\n\nFailure level : WorkerNode\nPanel : Not Running Pods 0:OK\nDataSource : Prometheus\nResource : pod\nThreshold : not running pod count > 0 , every 5m , for 5m",
                "tags": {

                }
            }
        }
        params3 = {
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
                        "tags": None
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

        params4 = {
            "options": {

            },
            "data": {
                "ruleId": 22.0,
                "orgId": 1.0,
                "ruleName": "API Server Request Latency TEMP",
                "dashboardId": 10.0,
                "message": "Temporary test Webhook\n- API Server Request Latency",
                "imageUrl": "https://grafana.stargate.cloudeco.io/public/img/attachments/qmNDGfjVSyG53lu9RmOb.png",
                "evalMatches": [
                    {
                        "tags": {
                            "pod": "plugin-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9",
                            "LB": "plugin-grafana-monitoring-webhook-rajbcnsjbhjszvfv-jps-8b84876q9wq9"
                        },
                        "metric": "plugin-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9",
                        "value": 0.15384615384615385
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
        params5 = {"options": {

            },
            "data": {}

        }
        #params1, params2, params3, params4,
        test_cases = [params5]

        for idx, test_case in enumerate(test_cases):
            print(f'###### {idx} ########')
            parsed_data = self.monitoring.Event.parse({'options': {}, 'data': test_case.get('data')})
            print_json(parsed_data)
            print()



if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
