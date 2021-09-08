from spaceone.core.error import *


class ERROR_REQUIRED_FIELDS(ERROR_BASE):
    _message = 'Required field is missing(field= {field})'


class ERROR_CHECK_VALIDITY(ERROR_BASE):
    _message = 'Event model is not validate (field= {field})'


class ERROR_PARSE_EVENT(ERROR_BASE):
    _message = 'Failed to parse event'


class ERROR_CONVERT_DATA_TYPE(ERROR_BASE):
    _message = 'Failed to convert data type'
