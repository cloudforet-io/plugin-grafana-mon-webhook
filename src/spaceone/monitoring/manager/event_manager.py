import logging
import requests
from spaceone.core.manager import BaseManager
from spaceone.monitoring.error import *
_LOGGER = logging.getLogger(__name__)


class EventManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, raw_data):
        default_parsed_data = []

        request = raw_data.get('request', {})
        header = request.get('header', {})

        ### TODO:: Add a Parsing logic on here

        return default_parsed_data
