import logging
import hashlib
import json
from datetime import datetime

from spaceone.core import utils
from plugin.manager.event_manager import ParseManager
from plugin.error import *

_LOGGER = logging.getLogger("spaceone")


class LegacyManager(ParseManager):
    webhook_type = "LEGACY"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data: dict
        :return EventsResponse: {
            "results": EventResponse
        }
        """
        results = []
        event: dict = {
            "event_key": self.generate_event_key(raw_data),
            "event_type": self.get_event_type(raw_data.get("state", "")),
            "severity": self.get_severity(raw_data.get("state", "")),
            "title": self.remove_alert_code_from_title(raw_data.get("title")),
            "rule": raw_data.get("ruleName", ""),
            "image_url": raw_data.get("imageUrl", ""),
            "resource": {},
            "description": raw_data.get("message", ""),
            "occurred_at": utils.datetime_to_iso8601(datetime.now()),
            "additional_info": self.get_additional_info(raw_data),
        }
        results.append(event)
        _LOGGER.debug(f"[LegacyParseManager] parse Event : {event}")

        return {"results": results}

    def generate_event_key(self, raw_data: dict) -> str:
        dashboard_id = raw_data.get("dashboardId")
        panel_id = raw_data.get("panelId")
        rule_id = raw_data.get("ruleId")
        org_id = raw_data.get("orgId")

        if dashboard_id is None:
            raise ERROR_REQUIRED_FIELDS(field="dashboard_id")

        if panel_id is None:
            raise ERROR_REQUIRED_FIELDS(field="panel_id")

        if rule_id is None:
            raise ERROR_REQUIRED_FIELDS(field="rule_id")

        if org_id is None:
            raise ERROR_REQUIRED_FIELDS(field="org_id")

        # Event key generation
        event_key = f"{dashboard_id}:{panel_id}:{rule_id}:{org_id}"
        hash_object = hashlib.md5(event_key.encode())
        hashed_event_key = hash_object.hexdigest()

        return hashed_event_key

    def get_event_type(self, event_state: str) -> str:
        return "RECOVERY" if event_state == "ok" else "ALERT"

    def get_severity(self, event_state: str) -> str:
        """
        alerting : ALERT
        ok : RECOVERY
        no_data : NONE
        ------
        paused: Cannot be notified as a event_state.
        pending: Cannot be notified as event_state.
        """
        severity_flag = "NONE"
        if event_state == "ok":
            severity_flag = "INFO"
        elif event_state == "no_data":
            severity_flag = "NONE"
        elif event_state == "alerting":
            severity_flag = "ERROR"

        return severity_flag

    def get_additional_info(self, raw_data: dict) -> dict:
        additional_info = {}
        if "dashboardId" in raw_data:
            additional_info.update(
                {"dashboard_id": str(raw_data.get("dashboardId", ""))}
            )

        if "panelId" in raw_data:
            additional_info.update({"panel_id": str(raw_data.get("panelId"))})

        if "orgId" in raw_data:
            additional_info.update({"org_id": str(raw_data.get("orgId", ""))})

        if "ruleUrl" in raw_data:
            additional_info.update({"rule_url": raw_data.get("ruleUrl")})

        if "evalMatches" in raw_data:
            eval_match_dict = raw_data.get("evalMatches")
            eval_match_str = self.change_eval_dict_to_str(eval_match_dict)
            additional_info.update({"eval_matches": eval_match_str})

        return additional_info

    def remove_alert_code_from_title(self, title: str) -> str:
        try:
            alert_codes = ["[Alerting]", "[OK]", "[No Data]"]
            for alert_code in alert_codes:
                if alert_code in title:
                    title = title.replace(alert_code, "")
            return title

        except ValueError:
            raise ERROR_CONVERT_DATA_TYPE()

    def change_eval_dict_to_str(self, eval_matches: dict) -> str:
        try:
            eval_matches = json.dumps(eval_matches)
            return eval_matches

        except Exception as e:
            raise ERROR_CONVERT_DATA_TYPE(field=e)
