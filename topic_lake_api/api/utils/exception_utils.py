from starlette import status

from topic_lake_api.domain.constants import ApplicationExceptionReason
from topic_lake_api.domain.exceptions import ApplicationException


def status_code_from_application_exception(exc: ApplicationException) -> int:
    match exc.reason:
        case ApplicationExceptionReason.ALREADY_EXISTS:
            return status.HTTP_409_CONFLICT
        case ApplicationExceptionReason.DOES_NOT_EXISTS:
            return status.HTTP_404_NOT_FOUND
        case ApplicationExceptionReason.INVALID_INPUT:
            return status.HTTP_400_BAD_REQUEST
        case ApplicationExceptionReason.FORBIDDEN_ACTION:
            return status.HTTP_403_FORBIDDEN
        case _:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
