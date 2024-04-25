import json
import logging
import hashlib
import re
from typing import List

from spaceone.core import utils
from plugin.manager.event_manager import ParseManager
from plugin.error import (
    ERROR_REQUIRED_FIELDS,
)

_LOGGER = logging.getLogger("spaceone")


class AWSSNSManager(ParseManager):
    webhook_type = "AWS_SNS"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data: dict
        :return EventResponse: {
           "results": EventResponse
        }
        """
        results = []
        _LOGGER.debug(f"[AWSSNSManager] data => {raw_data}")
        event: dict = {
            "event_key": self.generate_event_key(raw_data),
            "event_type": self.get_event_type(""),
            "severity": self.get_severity(""),
            "title": raw_data.get("Type", ""),
            "rule": "",
            "image_url": raw_data.get("SubscribeURL", ""),
            "resource": {},
            "description": self._get_message(raw_data),
            "occurred_at": self.convert_to_iso8601(raw_data.get("Timestamp")),
            "additional_info": self.get_additional_info(raw_data),
        }
        results.append(event)
        _LOGGER.debug(f"[AWSSNSManager] parse Event : {event}")

        return {"results": results}

    def generate_event_key(self, raw_data: dict) -> str:
        group_key = raw_data.get("TopicArn")

        if group_key is None:
            raise ERROR_REQUIRED_FIELDS(field="group_key")
        hash_object = hashlib.md5(group_key.encode())
        hashed_event_key = hash_object.hexdigest()

        return hashed_event_key

    def _get_message(self, raw_data: dict) -> str:
        raw_data = utils.get_dict_value(raw_data, "Message")
        raw_data = json.loads(raw_data)

        message = utils.get_dict_value(raw_data, "detail.message")
        filtered_message = self.__remove_keys(
            message, ["Annotations", "Source", "Silence"]
        )
        no_value_data = re.search(r"\[no value\]", filtered_message)

        if no_value_data:
            filtered_message += "DatasourceNoData\n"
        else:
            alerts = utils.get_dict_value(raw_data, "detail.alerts")

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
        return re.sub(pattern, "", text, flags=re.MULTILINE)

    def get_event_type(self, event_state: str) -> str:
        return "ALERT"

    def get_severity(self, event_state: str) -> str:
        return "INFO"

    def get_additional_info(self, raw_data: dict) -> dict:
        return {
            "Timestamp": self.convert_to_iso8601(raw_data.get("Timestamp")),
            "MessageId": raw_data.get("MessageId"),
            "SigningCertURL": raw_data.get("SigningCertURL"),
            "Signature": raw_data.get("Signature"),
            "SignatureVersion": raw_data.get("SignatureVersion"),
            "Type": raw_data.get("Type"),
            "Message": raw_data.get("Message"),
            "Token": raw_data.get("Token"),
            "TopicArn": raw_data.get("TopicArn"),
            "SubscribeURL": raw_data.get("SubscribeURL"),
        }

    def remove_alert_code_from_title(self, title):
        pass

    def change_eval_dict_to_str(self, eval_matches_dict):
        pass
