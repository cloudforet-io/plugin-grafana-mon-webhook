import logging
import hashlib
from spaceone.core import utils
from datetime import datetime
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *
_LOGGER = logging.getLogger(__name__)
_INTERVAL_IN_SECONDS = 600
_EXCEPTION_TO_PASS = ["Test notification"]


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, raw_data):

        default_parsed_data = []

        try:
            eval_match_values = raw_data.get('evalMatches', [])
            occurred_at = datetime.now()
            event_key = self._get_event_key(raw_data, occurred_at)
            event_type = self._get_event_type(raw_data)
            severity = self._get_severity(raw_data)
            description = raw_data.get('message', '')
            title = raw_data.get('title', '')
            rule_name = raw_data.get('ruleName', '')
            # Check Eval Matched Value is Empty

            event_vo = {
                'event_key': event_key,
                'event_type': event_type,
                'severity': severity,
                'title': title,
                'rule': rule_name,
                'resource': {},
                'description': description,
                'occurred_at': occurred_at,
                'additional_info': self._get_additional_info(raw_data)
            }

            if len(eval_match_values) == 0:
                _LOGGER.debug(f'[EventManager] parse Event : {event_vo}')
                self._check_validity_and_append(default_parsed_data, event_vo)
            else:
                for eval_match_value in eval_match_values:
                    if self._check_required_to_parse(eval_match_value):
                        tags_dict = eval_match_value.get('tags')
                        for tag_dict in tags_dict:
                            inner_resource = {
                                'name': f'[{tag_dict}]:{tags_dict.get(tag_dict)}',
                                'resource_type': tag_dict,
                                'resource_id': tags_dict.get(tag_dict)
                            }
                            event_vo.update({'resource': inner_resource})
                            _LOGGER.debug(f'[EventManager] parse Event : {event_vo}')
                            self._check_validity_and_append(default_parsed_data, event_vo)
                    else:
                        event_resource = self._get_resource_for_event(eval_match_value, raw_data)
                        event_vo.update({'resource': event_resource})
                        _LOGGER.debug(f'[EventManager] parse Event : {event_vo}')
                        self._check_validity_and_append(default_parsed_data, event_vo)

        except Exception as e:
            generated = utils.generate_id('grafana', 4)
            hash_object = hashlib.md5(generated.encode())
            md5_hash = hash_object.hexdigest()
            error_message = repr(e)
            event_vo = {
                'event_key': md5_hash,
                'event_type': 'ALERT',
                'severity': 'CRITICAL',
                'resource': {},
                'description': error_message,
                'title': 'Grafana Parsing ERROR',
                'rule': '',
                'occurred_at': datetime.now(),
                'additional_info': {}
            }
            self._check_validity_and_append(default_parsed_data, event_vo)
        return default_parsed_data

    @staticmethod
    def _get_event_key(raw_data, occurred_at):
        dashboard_id = raw_data.get('dashboardId')
        panel_id = raw_data.get('panelId')
        rule_id = raw_data.get('ruleId')
        org_id = raw_data.get('orgId')
        indexed_unique_key = None

        if dashboard_id is None:
            raise ERROR_REQUIRED_FIELDS(field='dashboard_id')

        if panel_id is None:
            raise ERROR_REQUIRED_FIELDS(field='panel_id')

        if rule_id is None:
            raise ERROR_REQUIRED_FIELDS(field='rule_id')

        if org_id is None:
            raise ERROR_REQUIRED_FIELDS(field='org_id')


        if isinstance(occurred_at, datetime):
            occurred_at_timestamp = str(occurred_at.timestamp())
            _occurred_at_timestamp = occurred_at_timestamp[:occurred_at_timestamp.find('.')]
            str_to_int = float(_occurred_at_timestamp) if len(_occurred_at_timestamp) > 10 else int(_occurred_at_timestamp)
            indexed_unique_key = int(str_to_int) // _INTERVAL_IN_SECONDS

        raw_event_key = f'{dashboard_id}:{panel_id}:{rule_id}:{org_id}:{indexed_unique_key}'
        hash_object = hashlib.md5(raw_event_key.encode())
        md5_hash = hash_object.hexdigest()

        return md5_hash

    @staticmethod
    def _get_event_type(raw_data):
        """
        alerting: ALERT
        no_data: ALERT
        pending: ALERT
        ok: RECOVERY
        paused: ALERT
        """
        event_state = raw_data.get('state')
        return 'RECOVERY' if event_state == 'ok' else 'ALERT'

    @staticmethod
    def _get_severity(raw_data):
        event_state = raw_data.get('state')
        default_severity_flag = 'NOT_AVAILABLE'
        if event_state == 'ok':
            default_severity_flag = 'INFO'
        elif event_state in ['alerting', 'pending', 'paused']:
            default_severity_flag = 'ERROR'

        return default_severity_flag

    @staticmethod
    def _get_additional_info(raw_data):

        additional_info = {}
        if 'dashboardId' in raw_data:
            additional_info.update({'dashboard_id': str(raw_data.get('dashboardId', ''))})

        if 'panelId' in raw_data:
            additional_info.update({'panel_id': str(raw_data.get('panelId'))})

        if 'orgId' in raw_data:
            additional_info.update({'org_id': str(raw_data.get('orgId', ''))})

        if 'imageUrl' in raw_data:
            additional_info.update({'image_url': raw_data.get('imageUrl')})

        if 'ruleUrl' in raw_data:
            additional_info.update({'rule_url': raw_data.get('ruleUrl')})

        return additional_info

    @staticmethod
    def _get_resource_for_event(eval_value, raw_data):
        event_resource = {}
        tags = eval_value.get('tags')
        if tags is None:
            event_resource.update({'name': 'unavailable resource'})
        else:
            resource_types = [tag for tag in tags]
            resource_values = [t for t in tags.values()]
            _resource_types_str = '&'.join(resource_types) if len(resource_types) > 0 else ''
            event_resource.update({
                'name': f'[{_resource_types_str}]:{resource_values[0]}',
                'resource_type': _resource_types_str,
                'resource_id': resource_values[0]
            })

        return event_resource

    @staticmethod
    def _check_required_to_parse(eval_value):
        required_to_mimic = False
        tags = eval_value.get('tags')
        if tags is None:
            pass
        else:
            resource_values = [t for t in tags.values()]
            if len(resource_values) > 1 and len(resource_values) != resource_values.count(resource_values[0]):
                required_to_mimic = True
        return required_to_mimic

    @staticmethod
    def _check_test_notification(raw_data):
        notification_state_to_process = False
        rule_name = raw_data.get('ruleName')
        if rule_name in _EXCEPTION_TO_PASS:
            notification_state_to_process = True
        return notification_state_to_process

    @staticmethod
    def _check_validity_and_append(append_list, check_data):
        event_result_model = EventModel(check_data, strict=False)
        event_result_model.validate()
        event_result_model_primitive = event_result_model.to_native()
        append_list.append(event_result_model_primitive)
