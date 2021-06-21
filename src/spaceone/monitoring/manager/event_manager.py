import logging
import hashlib
from datetime import datetime
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel

_LOGGER = logging.getLogger(__name__)
_INTERVAL_IN_SECONDS = 600
_EXCEPTION_TO_PASS = ["Test notification", "null", "Null"]

class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, raw_data):

        # check test notification for skip
        #"ruleName": "Test notification", "title": "[Alerting] Test notification", "ruleUrl": "https://grafana.stargate.cloudeco.io/"

        default_parsed_data = []
        eval_match_values = raw_data.get('evalMatches', [])
        occurred_at = datetime.now()

        for eval_match_value in eval_match_values:
            target_types, title, instance_id = self._get_alarm_title_type_instance_id(raw_data, eval_match_value)

            event_key = self._get_event_key(raw_data,  occurred_at, instance_id)
            event_resource = self._get_resource_for_event(eval_match_value, {}, target_types, instance_id, raw_data)

            event_vo = {
                'event_key': event_key,
                'event_type': self._get_event_type(raw_data),
                'severity': self._get_severity(raw_data),
                'resource': event_resource,
                'description': raw_data.get('message', ''),
                'title': title,
                'occurred_at': occurred_at,
                'rule': self._get_rule_for_event(raw_data),
                'additional_info': self._get_additional_info(raw_data)
            }

            _LOGGER.debug(f'[EventManager] parse Event : {event_vo}')
            event_result_model = EventModel(event_vo, strict=False)
            event_result_model.validate()
            event_result_model_primitive = event_result_model.to_native()
            default_parsed_data.append(event_result_model_primitive)

        return default_parsed_data

    @staticmethod
    def _get_rule_for_event(raw_data):
        return raw_data.get('ruleName')

    @staticmethod
    def _get_event_key(raw_data, occurred_at, instance_id):
        dashboard_id = raw_data.get('dashboardId')
        panel_id = raw_data.get('panelId')
        rule_id = raw_data.get('ruleId')
        indexed_unique_key = None

        if isinstance(occurred_at, datetime):
            occurred_at_timestamp = str(occurred_at.timestamp())
            _occurred_at_timestamp = occurred_at_timestamp[:occurred_at_timestamp.find('.')]
            str_to_int = float(_occurred_at_timestamp) if len(_occurred_at_timestamp) > 10 else int(_occurred_at_timestamp)
            indexed_unique_key = int(str_to_int) // _INTERVAL_IN_SECONDS * 100

        raw_event_key = f'{dashboard_id}:{panel_id}:{rule_id}:{instance_id}:{indexed_unique_key}'
        hash_object = hashlib.md5(raw_event_key.encode())
        md5_hash = hash_object.hexdigest()

        return md5_hash

    @staticmethod
    def _get_event_type(raw_data):
        event_state = raw_data.get('state', 'no_data')
        return 'RECOVERY' if event_state == 'ok' else 'ALERT'

    @staticmethod
    def _get_severity(raw_data):
        event_state = raw_data.get('state')
        default_severity_flag = 'NOT_AVAILABLE'
        if event_state == 'ok':
            default_severity_flag = 'INFO'
        elif event_state == 'alerting':
            default_severity_flag = 'ERROR'

        return default_severity_flag

    @staticmethod
    def _get_additional_info(raw_data):
        tags = {}

        if 'imageUrl' in raw_data:
            tags.update({'image_url': raw_data.get('imageUrl')})

        if 'orgId' in raw_data:
            tags.update({'org_id': str(raw_data.get('orgId', ''))})

        if 'ruleUrl' in raw_data:
            tags.update({'rule_url': raw_data.get('ruleUrl')})

        if 'dashboardId' in raw_data:
            tags.update({'dashboard_id': str(raw_data.get('dashboardId', ''))})

        return tags

    @staticmethod
    def _get_resource_for_event(eval_value, event_resource, resource_type, instance_id, raw_data):
        tags = eval_value.get('tags', {})
        if tags is None:
            dashboard_id = str(raw_data.get('dashboardId', ''))
            panel_id = str(raw_data.get('panelId', ''))
            org_id = str(raw_data.get('orgId', ''))
            _instance_id = f'{dashboard_id}{panel_id}{org_id}'
            if instance_id == _instance_id:
                event_resource.update({
                    'resource_id': f'[{resource_type}], Dashboard ID: {dashboard_id}, Panel ID: {panel_id}',
                    'resource_type': resource_type,
                })
        else:
            for idx, tag in enumerate(tags):
                if idx == 0:
                    event_id = tags.get(tag)
                    event_resource.update({
                        'resource_type': resource_type,
                        'resource_id': event_id
                    })
                    break

        return event_resource

    @staticmethod
    def _check_test_notification(raw_data):
        notification_state_to_process = False
        rule_name = raw_data.get('ruleName')
        if rule_name in _EXCEPTION_TO_PASS:
            notification_state_to_process = True
        return notification_state_to_process

    @staticmethod
    def _is_invalid_to_proceed(eval_value):
        tags = eval_value.get('tags')
        is_invalid = True

        if tags is None or tags in _EXCEPTION_TO_PASS:
            pass
        else:
            is_invalid = False

        return is_invalid

    @staticmethod
    def _get_alarm_title_type_instance_id(raw_data, eval_value):
        tags = eval_value.get('tags', {})
        title = raw_data.get('title', '')
        target_types = []
        instance_id = None
        if tags is None:
            dashboard_id = str(raw_data.get('dashboardId', ''))
            panel_id = str(raw_data.get('panelId', ''))
            org_id = str(raw_data.get('orgId', ''))
            instance_id = f'{dashboard_id}{panel_id}{org_id}'
            return 'UNKNOWN', title, instance_id
        else:
            for idx, tag in enumerate(tags):
                if idx == 0:
                    instance_id = tags.get(tag)
                target_types.append(tag)

            return '' if len(target_types) == 0 else '&'.join(target_types), title, instance_id
