from enum import Enum


class ApplicationExceptionReason(Enum):
    ALREADY_EXISTS = 1
    DOES_NOT_EXISTS = 2
