from topic_recommendations.interactor.constants import ApplicationExceptionReason


class ApplicationException(Exception):
    def __init__(self, reason: ApplicationExceptionReason, message: str):
        self.reason = reason
        self.message = message


class AlreadyExist(ApplicationException):
    def __init__(self, message: str):
        super().__init__(ApplicationExceptionReason.ALREADY_EXISTS, message)


class DoesNotExist(ApplicationException):
    def __init__(self, message: str):
        super().__init__(ApplicationExceptionReason.DOES_NOT_EXISTS, message)


class InvalidInputData(ApplicationException):
    def __init__(self, message: str):
        super().__init__(ApplicationExceptionReason.INVALID_INPUT, message)
