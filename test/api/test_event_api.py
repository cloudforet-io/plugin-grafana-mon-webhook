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

                    "evalMatches": [
                        {
                            "metric": "Count",
                            "tags": {},
                            "value": 24.0
                        }
                    ],
                    "orgId": 1.0,
                    "title": "[Alerting] Database Size alert",
                    "ruleId": 93.0,
                    "dashboardId": 58.0,
                    "tags": {
                        "jiji": "yoon"
                    },
                    "ruleName": "Database Size alert",
                    "panelId": 5.0,
                    "ruleUrl": "https://grafana.stargate.cloudeco.io/d/9tvNgo77k/mongodb-database-details_copy-20210818?tab=alert&viewPanel=5&orgId=1",
                    "message": "데이터베이스~",
                    "state": "alerting"
                }

        }
        params2 = {
            "options": {

            },
            "data": {
                "evalMatches": [
                    {
                        "tags": {
                            "pod": "grpc-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9"
                        },
                        "metric": "grpc-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9",
                        "value": 0.15384615384615385
                    }
                ],
                "imageUrl": "https://grafana.stargate.cloudeco.io/public/img/attachments/yo4maLzA629Oh24c1g1g.png",
                "ruleId": 57.0,
                "title": "[Alerting] Not Running Pods 0:OK alert",
                "panelId": 58.0,
                "state": "alert",
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
                "evalMatches": [],
                "dashboardId": 44.0,
                "panelId": 14.0,
                "orgId": 1.0,
                "ruleName": "Kubelet Runtime Operations Error Rate alert",
                "state": "ok",
                "tags": {},
                "title": "[OK] Kubelet Runtime Operations Error Rate alert",
                "ruleUrl": "https://grafana.stargate.cloudeco.io/d/6eRS6XR7k/spaceone-dev-cluster-alerts-dashboard-20210621-backup?tab=alert&viewPanel=14&orgId=1",
                "ruleId": 92.0
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
                            "pod": "grpc-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9",
                            "LB": "grpc-grafana-monitoring-webhook-rajbcnsjbhjszvfv-jps-8b84876q9wq9"
                        },
                        "metric": "grpc-grafana-monitoring-webhook-rajbcnsjbhjszvfv-8b84876q9wq9",
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
            "data": {
                "evalMatches": [
                    {
                        "tags": {},
                        "value": 0.020317392596204395,
                        "metric": "{}"
                    }
                ],
                "ruleId": 92.0,
                "ruleName": "Kubelet Runtime Operations Error Rate alert",
                "tags": {},
                "dashboardId": 44.0,
                "orgId": 1.0,
                "panelId": 14.0,
                "state": "alerting",
                "title": "[Alerting] Kubelet Runtime Operations Error Rate alert",
                "ruleUrl": "https://grafana.stargate.cloudeco.io/d/6eRS6XR7k/spaceone-dev-cluster-alerts-dashboard-20210621-backup?tab=alert&viewPanel=14&orgId=1"
            }

        }
        params6 = {
            "options": {},
            "data": {

                "panelId": 8.0,
                "orgId": 1.0,
                "title": "[Alerting] API Server Request Errors alert",
                "ruleName": "API Server Request Errors alert",
                "tags": {},
                "message": "API Server Request Errors",
                "evalMatches": [
                    {
                        "tags": {
                            "code": "0",
                            "verb": "WATCH"
                        },
                        "metric": "0 WATCH",
                        "value": 0.7647628374624433
                    }, {
                        "tags": {
                            "verb": "POST",
                            "code": "201"
                        },
                        "metric": "201 POST",
                        "value": 0.43159030922294406
                    }
                ],
                "dashboardId": 44.0,
                "state": "alerting",
                "ruleUrl": "https://grafana.stargate.cloudeco.io/d/6eRS6XR7k/spaceone-dev-cluster-alerts-d" +
                           "ashboard-20210621-backup?tab=alert&viewPanel=8&orgId=1",
                "ruleId": 90.0

            }
        }

        params7 = {
            "options": {},
            "data":
                {
                    "ruleUrl": "https://grafana.stargate.cloudeco.io/d/6eRS6XR7k/spaceone-dev-cluster-alerts-dashboard-20210621-backup?tab=alert&viewPanel=16&orgId=1",
                    "evalMatches": [
                        {
                            "tags": {
                                "verb": "GET"
                            },
                            "value": 0.00953699724356614,
                            "metric": "GET"
                        },
                        {
                            "value": 0.010471153199535389,
                            "metric": "PUT",
                            "tags": {
                                "verb": "PUT"
                            }
                        },
                        {
                            "value": 0.003164335949212073,
                            "metric": "POST",
                            "tags": {
                                "verb": "POST"
                            }
                        }
                    ],
                    "ruleName": "API Server Rest Client Request Latency alert",
                    "orgId": 1.0,
                    "ruleId": 81.0,
                    "message": "detail msg",
                    "title": "[Alerting] API Server Rest Client Request Latency alert",
                    "state": "alerting",
                    "tags": {},
                    "dashboardId": 44.0,
                    "panelId": 16.0
                }
        }
        params8 = {
            'options': {},
            'data': {

                    "occured_at": "2021-08-23T06:47:42.759Z",
                    "description": "마이데이타 포탈 테스트의CPU 현재 주의 상태",
                    "title": "(주의 알림)마이데이타 포탈 테스트/CPU",
                    "event_type": "ALERT",
                    "severity": "ALERT",
                    "alert_id": "alert-f81100e73c00"
                }
            }
        params9 = {
            'options':{},
            'data':{

                    "orgId": 1.0,
                    "tags": {
                        "tag name": "tag value"
                    },
                    "title": "[Alerting]jiyoonkii_Test Panel Title alert",
                    "state": "alerting",
                    "dashboardId": 1.0,
                    "ruleUrl": "http://localhost:3000/d/hZ7BuVbWz/test-dashboard?fullscreen&edit&tab=alert&panelId=2&orgId=1",
                    "ruleName": "Panel Title alert",
                    "ruleId": 1.0,
                    "panelId": 2.0,
                    "message": "Notification Message",
                    "evalMatches": [
                        {
                            "tags": {},
                            "metric": "Count",
                            "value": 1.0
                        }
                    ],
                    "imageUrl": "https://grafana.com/assets/img/blog/mixed_styles.png"
                }
        }
        #params1, params2, params3, params4,
        test_cases = [params9]

        for idx, test_case in enumerate(test_cases):
            print(f'###### {idx} ########')
            data = test_case.get('data')
            parsed_data = self.monitoring.Event.parse({'options': {}, 'data': data})
            print(parsed_data)



if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
