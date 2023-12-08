import logging
from abc import abstractmethod, ABCMeta

from spaceone.core.manager import BaseManager
from plugin.error import *

__all__ = ['ParseManager']
_LOGGER = logging.getLogger('spaceone')


class ParseManager(BaseManager, metaclass=ABCMeta):

    webhook_type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    @abstractmethod
    def parse(self, **kwargs):
        pass

    @abstractmethod
    def generate_event_key(self, **kwargs):
        pass

    @abstractmethod
    def get_event_type(self, event_state):
        pass

    @abstractmethod
    def get_severity(self, event_state):
        pass

    @abstractmethod
    def get_additional_info(self, **kwargs):
        pass

    @abstractmethod
    def remove_alert_code_from_title(self, title):
        pass

    @abstractmethod
    def change_eval_dict_to_str(self, eval_matches_dict):
        pass

    @classmethod
    def get_parse_manager_by_webhook_type(cls, webhook_type):
        for subclass in cls.__subclasses__():
            if subclass.webhook_type == webhook_type:
                return subclass()
        raise ERROR_INVALID_WEBHOOK_TYPE(webhook_type=webhook_type)
