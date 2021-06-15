import logging
import hashlib
from datetime import datetime
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel

_LOGGER = logging.getLogger(__name__)
_INTERVAL_IN_SECONDS = 600
_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'


class EventManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, raw_data):
        default_parsed_data = []

        eval_match_values = raw_data.get('evalMatches', [])
        occurred_at = datetime.now()
        for eval_match_value in eval_match_values:
            target_types, title, instance_id = self._get_alarm_title_type(raw_data, eval_match_value)
            event_key = self._get_event_key(raw_data, occurred_at, instance_id)
            event_resource = self._get_resource_for_event(eval_match_value, {}, target_types)
            event_vo = {
                'event_key': event_key,
                'event_type': self._get_event_type(raw_data),
                'severity': self._get_severity(raw_data),
                'resource': event_resource,
                'description': raw_data.get('message', ''),
                'title': title,
                'rule': self._get_rule_for_event(raw_data),
                'tags': self._get_tags(raw_data)
            }

            _LOGGER.debug(f'[EventManager] parse Event : {event_vo}')
            event_result_model = EventModel(event_vo, strict=False)
            event_result_model.validate()
            event_result_model_primitive = event_result_model.to_primitive()
            event_result_model_primitive.update({'occurred_at': occurred_at})
            default_parsed_data.append(event_result_model_primitive)

        return default_parsed_data

    @staticmethod
    def _get_rule_for_event(raw_data):
        return raw_data.get('ruleName')

    @staticmethod
    def _get_event_key(raw_data, instance_id, occurred_at):
        # account_id:instance_id:alarm_name:date_time
        dashboard_id = raw_data.get('dashboardId')
        panel_id = raw_data.get('panelId')
        rule_id = raw_data.get('ruleId')
        indexed_unique_key = None

        if isinstance(occurred_at, datetime):
            occurred_at_timestamp = str(occurred_at.timestamp())
            indexed_unique_key = int(occurred_at_timestamp) // 600 * 100

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
    def _get_tags(raw_data):
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
    def _get_resource_for_event(eval_value, event_resource, resource_type):
        tags = eval_value.get('tags', {})
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
    def _get_alarm_title_type(raw_data, eval_value):
        alarm_name = raw_data.get('title', '')
        tags = eval_value.get('tags', {})
        target_types = []

        if not tags:
            return '' if not target_types else '&'.join(target_types), 'No title', ''
        else:

            instance_id = None
            for idx, tag in enumerate(tags):
                if idx == 0:
                    instance_id = tags.get(tag)
                target_types.append(tag)

            return '' if not target_types else '&'.join(target_types), f'[{instance_id}]: {alarm_name}', instance_id
