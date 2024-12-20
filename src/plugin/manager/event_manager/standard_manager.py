import hashlib
import logging
from datetime import datetime
from typing import Union, List

import regex
from spaceone.core import utils

from plugin.error import (
    ERROR_REQUIRED_FIELDS,
    ERROR_CONVERT_TITLE,
    ERROR_CONVERT_DATA_TYPE,
)
from plugin.manager.event_manager import ParseManager

_LOGGER = logging.getLogger("spaceone")


class StandardManager(ParseManager):
    webhook_type = "STANDARD"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data: dict
        :return EventsResponse: {
            "results": EventResponse
        }
        """
        results = []
        _LOGGER.debug(f"[StandardManager] data => {raw_data}")
        event: dict = {
            "event_key": self.generate_event_key(raw_data),
            "event_type": self.get_event_type(raw_data.get("status", "")),
            "severity": self.get_severity(raw_data.get("status", "")),
            "title": self._get_title(raw_data),
            "rule": self._get_rule(raw_data),
            "image_url": self._get_value_from_alerts(raw_data, "panelURL"),
            "resource": {},
            "description": self._get_message(raw_data),
            "occurred_at": self.convert_to_iso8601(
                self._get_value_from_alerts(raw_data, "startsAt")
            ),
            "additional_info": self.get_additional_info(raw_data),
        }
        results.append(event)
        _LOGGER.debug(f"[StandardManager] parse Event : {event}")

        return {"results": results}

    def generate_event_key(self, raw_data: dict) -> str:
        group_key = raw_data.get("groupKey")

        if group_key is None:
            raise ERROR_REQUIRED_FIELDS(field="group_key")
        hash_object = hashlib.md5(group_key.encode())
        hashed_event_key = hash_object.hexdigest()

        return hashed_event_key

    def get_event_type(self, event_status: str) -> str:
        """
        firing : ALERT
        resolved : RECOVERY
        :param event_status:
        :return:
        """
        return "RECOVERY" if event_status == "resolved" else "ALERT"

    def get_severity(self, event_status: str) -> str:
        """
        firing : ERROR
        resolved : INFO
        :param event_status:
        :return:
        """
        severity_flag = "NONE"

        if event_status == "resolved":
            severity_flag = "INFO"
        elif event_status == "firing":
            severity_flag = "ERROR"

        return severity_flag

    def _get_message(self, raw_data: dict) -> str:
        message = utils.get_dict_value(raw_data, "message")

        no_value_data = regex.search(r"\[no value\]", message)
        if no_value_data:
            return "DatasourceNoData"
        else:
            filtered_message = self.__remove_keys(
                message, ["Annotations", "Source", "Silence"]
            )
            alerts = utils.get_dict_value(raw_data, "alerts")
            filtered_message = regex.sub(r"\n{3,}", "\n\n", filtered_message)

            filtered_message += "ValueString: \n"
            for alert in alerts:
                value_string = utils.get_dict_value(alert, "valueString")
                elements = value_string.split(", ")

                for element in elements:
                    filtered_message += f"- {element}\n"

                filtered_message += "\n"

            return filtered_message

    @staticmethod
    def __remove_keys(text: str, keys: List[str]) -> str:
        pattern = r"|".join(rf"{key}:\s+.*" for key in keys)
        return regex.sub(pattern, "", text, flags=regex.MULTILINE)

    def get_additional_info(self, raw_data: dict) -> dict:
        additional_info = {}
        for label in raw_data.get("commonLabels", {}).keys():
            additional_info.update(
                {label: str(raw_data.get("commonLabels", {}).get(label, ""))}
            )

        return additional_info

    def _get_title(self, raw_data: dict) -> str:
        if raw_data.get("commonLabels", {}).get("alertname") is None:
            return self.remove_alert_code_from_title(raw_data.get("title"))
        else:
            return raw_data.get("commonLabels", {}).get("alertname", " ")

    def remove_alert_code_from_title(self, title: str) -> str:
        """
        title template
        - [FIRING:4, RESOLVED:4] xxx
        - [FIRING:4] xxx
        - [RESOLVED:4] xxx

        :param title:
        :return:
        """
        try:
            title = regex.sub(
                r"\[(FIRING|RESOLVED):(\d+),? ?(FIRING|RESOLVED)?:?(\d+)?\]", "", title
            )
            title = regex.sub(r"\[([a-zA-Z]+:\d+,\s*[a-zA-Z]+:\d+)\]\s", "", title)
        except Exception:
            ERROR_CONVERT_TITLE(title)

        return title

    def change_eval_dict_to_str(self, eval_matches: dict) -> str:
        try:
            eval_matches = utils.dump_json(eval_matches)
            return eval_matches
        except Exception as e:
            raise ERROR_CONVERT_DATA_TYPE(field=e)

    def _get_value_from_alerts(
        self, raw_data: dict, key: str
    ) -> Union[dict, datetime, str]:
        if self._get_alerts_cnt(raw_data) > 0:
            return raw_data.get("alerts")[0].get(key)
        else:
            if key == "startsAt":
                return datetime.now()
            return ""

    @staticmethod
    def _get_alerts_cnt(raw_data: dict) -> int:
        return len(raw_data.get("alerts", ""))

    """
    @staticmethod
    def _convert_to_iso8601(raw_time: str) -> Union[str, None]:
        return utils.datetime_to_iso8601(parser.parse(raw_time))
    """

    def _make_description(self, raw_data: dict) -> str:
        raw_description = raw_data.get("groupLabels", {})
        raw_description.update(raw_data.get("commonLabels", {}))
        raw_description.update(raw_data.get("commonAnnotations", {}))
        raw_description.update(externalURL=raw_data.get("externalURL", ""))
        raw_description.update(
            imageURL=self._get_value_from_alerts(raw_data, "panelURL")
        )
        # make dict to string
        description = ""
        for k in raw_description.keys():
            tmp = "".join([k.capitalize(), ": ", raw_description[k], "\n"])
            description += tmp

        return description

    @staticmethod
    def _get_rule(raw_data: dict) -> str:
        if raw_data.get("commonLabels", {}).get("rulename") is None:
            return raw_data.get("commonLabels", {}).get("alertname", " ")
        else:
            return raw_data.get("commonLabels", {}).get("rulename", " ")
