from fastapi import HTTPException
from starlette import status


class InternalException(Exception):
    pass


class InternalServerError(HTTPException):
    def __init__(self, message: str = ''):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


class BadRequest(HTTPException):
    def __init__(self, message: str = ''):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
