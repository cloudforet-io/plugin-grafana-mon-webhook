from spaceone.core.error import *


class ERROR_INVALID_WEBHOOK_TYPE(ERROR_INVALID_PARAMETER_TYPE):
    _message = 'Wrong Webhook Type(webhook_type= {webhook_type})'


class ERROR_CONVERT_TITLE(ERROR_BASE):
    _message = 'Failed to convert alert title'


class ERROR_REQUIRED_FIELDS(ERROR_BASE):
    _message = 'Required field is missing(field= {field})'


class ERROR_PARSE_EVENT(ERROR_BASE):
    _message = 'Failed to parse event'


class ERROR_CONVERT_DATA_TYPE(ERROR_BASE):
    _message = 'Failed to convert data type'

