import logging
from spaceone.core.service import *
from spaceone.monitoring.manager.event_manager import EventManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class EventService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_mgr: EventManager = self.locator.get_manager('EventManager')

    @transaction
    @check_required(['options', 'data'])
    def parse(self, params):
        """

        Args:
            params (dict): {
                'options': 'dict',
                'raw_data': 'dict'
            }

        Returns:
            plugin_metric_data_response (dict)
        """
        raw_data = params.get('data')
        parsed_event = self.event_mgr.parse(raw_data)
        _LOGGER.debug(f'[EventService: parse] {parsed_event}')
        return parsed_event
