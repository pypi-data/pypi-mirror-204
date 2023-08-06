"""
Common enums.
"""
from data_watch.common.base_enum import BaseEnum


class Status(BaseEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    IN_PROGRESS = "IN_PROGRESS"
    WARNING = "WARNING"


class Severity(BaseEnum):
    ERROR = "ERROR"
    WARN = "WARN"
