# plugin-grafana-monitoring-webhook
webhook for grafana

# Data Model

## Grafana Raw Data

Webhook notification: https://grafana.com/docs/grafana/latest/alerting/old-alerting/notifications/#webhook

~~~
{
  "dashboardId": 1,
  "evalMatches": [
    {
      "value": 1,
      "metric": "Count",
      "tags": {}
    }
  ],
  "ruleUrl": "https://grafana.stargate.cloudeco.io/d/6eRS6XR7k/spaceone-dev-cluster-alerts-dashboard-20210621-backup?tab=alert&viewPanel=14&orgId=1",
  "imageUrl": "https://grafana.com/assets/img/blog/mixed_styles.png",
  "message": "Notification Message",
  "orgId": 1,
  "panelId": 2,
  "ruleId": 1,
  "ruleName": "Panel Title alert",
  "ruleUrl": "http://localhost:3000/d/hZ7BuVbWz/test-dashboard?fullscreen\u0026edit\u0026tab=alert\u0026panelId=2\u0026orgId=1",
  "state": "alerting",
  "tags": {
    "tag name": "tag value"
  },
  "title": "[Alerting] Panel Title alert"
}
~~~

| Field 	| Example |
| ---   	| ---     |
| title		| Dastabase Size alert |
| message       | Database xxxxxx      |
| state  	| Alerting , ok , no_data |
| orgID		| 1			|
| ruleID	| 92			|
| dashboardID	|			|
| ruleName	| Database Size alert	|
| panelID	| 5			|
| ruleUrl	| https://grafana.stargate.cloudeco.io/d/9tvNgo77k/mongodb-database-details_copy-20210818?tab=alert&viewPanel=5&orgId=1 |
| ImageUrl	| https://grafana.stargate.cloudeco.io/d/9tvNgo77k/mongodb-database-details_copy-20210818?tab=alert&viewPanel=5&orgId=1 |
| tags		| { "a": "b" } 		|
| evalMatches	| "evalMatches": [{"value": 342.2222, "metric": "Count", "tags": null}] |


## SpaceONE Event Model

| Field		| Type | Description	| Example	|
| ---      | ---     | ---           | ---           |
| event_id | str  | auto generation | event-1234556  |
| event_key | str | hash key of raw_data.panel_id, dashboard_id, org_id | b5dfksdfjskfsdfklsf3423432dff |
| event_type |  str  | RECOVERY , ALERT based on raw_data.state | RECOVERY	|
| title | str	| raw_data.title	| [ALERT] Database Size alert	|
| description | str | raw_data.message	| Database xxxxxx		|
| severity | str  | alert level based raw_data.state (alerting  -> ALERT, ok -> RECOVERY, no_dat -> NONE | ALERT	|
| resource | dict | Not used		| N/A	|
| raw_data | dict | Grafana Raw Data | {"title": "Database Size Alert", "dashboardId": 1, ... } |
| addtional_info | dict | raw_data.dashboardID, raw_data.orgID, raw_data.imageUrl, raw_data.ruleUrl, raw_data.evalMatches, raw_data.tags 	| {"org_id": "1.0", "rule_url" "https://...." } |
| occured_at | datetime | webhook received time | "2021-08-23T06:47:32.753Z" |
| alert_id | str | mapped alert_id	| alert-3243434343 |
| webhook_id | str  | webhook_id	| webhook-34324234234234 |
| project_id | str	| project_id	| project-12312323232    |
| domain_id | str	| domain_id	| domain-12121212121	|
| created_at | datetime | created time | "2021-08-23T06:47:32.753Z"	|


## cURL Requests examples
This topic provides examples of calls to the SpaceONE Grafana monitoring webhook using cURL.

Here's a cURL command that works for getting the response from webhook, you can test the following on your local machine.
```
curl -X POST https://your_spaceone_monitoring_webhook_url -d '{
  "dashboardId": xx,
  "evalMatches": [
    {
      "value": xxx,
      "metric": "xxx",
      "tags": {}
    }
  ],
  "ruleUrl": "xxx",
  "imageUrl": "xxx",
  "message": "xxx",
  "orgId": xx,
  "panelId": xx,
  "ruleId": xx,
  "ruleName": "xxx",
  "ruleUrl": "xxx",
  "state": "xxx",
  "tags": {
    "xxx": "xxx"
  },
  "title": "xxx"
}
```

Followings are examples which works for testing your own webhook.

```
curl -X POST https://{your_spaceone_monitoring_grafana_webhook_url} -d '{
  "dashboardId": 1,
  "evalMatches": [
    {
      "value": 1,
      "metric": "Count",
      "tags": {}
    }
  ],
  "ruleUrl": "https://grafana.stargate.cloudeco.io/d/6eRS6XR7k/spaceone-dev-cluster-alerts-dashboard-20210621-backup?tab=alert&viewPanel=14&orgId=1",
  "imageUrl": "https://grafana.com/assets/img/blog/mixed_styles.png",
  "message": "Notification Message",
  "orgId": 1,
  "panelId": 2,
  "ruleId": 1,
  "ruleName": "Panel Title alert",
  "ruleUrl": "http://localhost:3000/d/hZ7BuVbWz/test-dashboard?fullscreen\u0026edit\u0026tab=alert\u0026panelId=2\u0026orgId=1",
  "state": "alerting",
  "tags": {
    "tag name": "tag value"
  },
  "title": "[Alerting] Panel Title alert"
}'
```

```
curl -X POST https://monitoring-webhook.dev.spaceone.dev/monitoring/v1/webhook/webhook-1eea0a98d2aa/ed270cc6ea8bb6037313ddbc1e6ee0b3/events -d '{
  "tags": {},
  "orgId": 0.0,
  "state": "alerting",
  "message": "Someone is testing the alert notification within Grafana.",
  "ruleUrl": "https://grafana.stargate.cloudeco.io/",
  "dashboardId": 1.0,
  "title": "[Alerting] Test notification",
  "panelId": 1.0,
  "ruleId": 3.2760766009712717e+18,
  "ruleName": "Test notification",
  "evalMatches": [
      {
          "metric": "High value",
          "tags": null,
          "value": 100.0
      },
      {
          "metric": "Higher Value",
          "value": 200.0,
          "tags": null
      }
  ]
}'
```