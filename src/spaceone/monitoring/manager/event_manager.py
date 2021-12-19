import logging
import hashlib
import json
from spaceone.core import utils
from datetime import datetime
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *
_LOGGER = logging.getLogger(__name__)
_EXCEPTION_TO_PASS = ["Test notification"]


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, raw_data):

        results = []

        occurred_at = datetime.now()
        event_key = self._generate_event_key(raw_data)
        event_type = self._get_event_type(raw_data.get('state', ''))
        severity = self._get_severity(raw_data.get('state', ''))
        description = raw_data.get('message', '')
        title = self._remove_alert_code_from_title(raw_data.get('title'))
        image_url = raw_data.get('imageUrl', '')
        rule_name = raw_data.get('ruleName', '')

        event_dict = {
            'event_key': event_key,
            'event_type': event_type,
            'severity': severity,
            'title': title,
            'rule': rule_name,
            'image_url': image_url,
            'resource': {},
            'description': description,
            'occurred_at': occurred_at,
            'additional_info': self._get_additional_info(self, raw_data)
        }

        event_vo = self._check_validity(event_dict)
        results.append(event_vo)
        _LOGGER.debug(f'[EventManager] parse Event : {event_dict}')

        return results

    @staticmethod
    def _generate_event_key(raw_data):
        dashboard_id = raw_data.get('dashboardId')
        panel_id = raw_data.get('panelId')
        rule_id = raw_data.get('ruleId')
        org_id = raw_data.get('orgId')

        if dashboard_id is None:
            raise ERROR_REQUIRED_FIELDS(field='dashboard_id')

        if panel_id is None:
            raise ERROR_REQUIRED_FIELDS(field='panel_id')

        if rule_id is None:
            raise ERROR_REQUIRED_FIELDS(field='rule_id')

        if org_id is None:
            raise ERROR_REQUIRED_FIELDS(field='org_id')

        # Event key generation
        event_key = f'{dashboard_id}:{panel_id}:{rule_id}:{org_id}'
        hash_object = hashlib.md5(event_key.encode())
        hashed_event_key = hash_object.hexdigest()

        return hashed_event_key

    @staticmethod
    def _get_event_type(event_state):
        return 'RECOVERY' if event_state == 'ok' else 'ALERT'

    @staticmethod
    def _get_severity(event_state):
        """
        alerting : ALERT
        ok : RECOVERY
        no_data : NONE
        ------
        paused: Cannot be notified as a event_state.
        pending: Cannot be notified as event_state.
        """
        severity_flag = 'NONE'
        if event_state == 'ok':
            severity_flag = 'INFO'
        elif event_state == 'no_data':
            severity_flag = 'NONE'
        elif event_state == 'alerting':
            severity_flag = 'ERROR'

        return severity_flag

    @staticmethod
    def _get_additional_info(self, raw_data):
        additional_info = {}
        if 'dashboardId' in raw_data:
            additional_info.update({'dashboard_id': str(raw_data.get('dashboardId', ''))})

        if 'panelId' in raw_data:
            additional_info.update({'panel_id': str(raw_data.get('panelId'))})

        if 'orgId' in raw_data:
            additional_info.update({'org_id': str(raw_data.get('orgId', ''))})

        if 'ruleUrl' in raw_data:
            additional_info.update({'rule_url': raw_data.get('ruleUrl')})

        if 'evalMatches' in raw_data:
            eval_match_dict = raw_data.get('evalMatches')
            eval_match_str = self._change_eval_dict_to_str(eval_match_dict)
            additional_info.update({'eval_matches': eval_match_str})

        return additional_info

    @staticmethod
    def _check_test_notification(raw_data):
        notification_state_to_process = False
        rule_name = raw_data.get('ruleName')
        if rule_name in _EXCEPTION_TO_PASS:
            notification_state_to_process = True
        return notification_state_to_process

    @staticmethod
    def _check_validity(event_dict):
        try:
            event_result_model = EventModel(event_dict, strict=False)
            event_result_model.validate()
            event_result_model_primitive = event_result_model.to_native()
            return event_result_model_primitive

        except Exception as e:
            raise ERROR_CHECK_VALIDITY(field=e)

    @staticmethod
    def _change_eval_dict_to_str(eval_matches_dict):
        try:
            eval_matches_str = json.dumps(eval_matches_dict)
            return eval_matches_str

        except Exception as e:
            raise ERROR_CONVERT_DATA_TYPE(field=e)

    @staticmethod
    def _remove_alert_code_from_title(title):
        try:
            alert_codes = ['[Alerting]', '[OK]', '[No Data]']
            for alert_code in alert_codes:
                if alert_code in title:
                    title = title.replace(alert_code, '')
            return title

        except ValueError:
            raise ERROR_CONVERT_DATA_TYPE()
