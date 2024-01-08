from starlette import status

from topic_recommendations.interactor.constants import ApplicationExceptionReason
from topic_recommendations.interactor.exceptions import ApplicationException


def status_code_from_application_exception(exc: ApplicationException) -> int:
    match exc.reason:
        case ApplicationExceptionReason.ALREADY_EXISTS:
            return status.HTTP_409_CONFLICT
        case ApplicationExceptionReason.DOES_NOT_EXISTS:
            return status.HTTP_404_NOT_FOUND
        case _:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
