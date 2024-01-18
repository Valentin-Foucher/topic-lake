import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from topic_lake_api.api.routes.connection import router as connection_router
from topic_lake_api.api.routes.items import router as items_router
from topic_lake_api.api.routes.topics import router as topics_router
from topic_lake_api.api.routes.users import router as users_router
from topic_lake_api.api.utils.exception_utils import status_code_from_application_exception
from topic_lake_api.exceptions import InternalException
from topic_lake_api.infra.db.core import init_db, shutdown_db
from topic_lake_api.interactor.exceptions import ApplicationException

logger = logging.getLogger(__name__)


def _internal_exception_handler(_, exc: InternalException) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
        'detail': str(exc)
    })


def _application_exception_handler(_, exc: ApplicationException) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(status_code=status_code_from_application_exception(exc), content={
        'detail': str(exc)
    })


def _fastapi_request_validation_error_handler(_, exc: RequestValidationError) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={
        'detail': [{'message': err['msg'], 'field': err['loc'][-1], 'value': err['input']} for err in exc.errors()]
    })


def add_error_handlers(app: FastAPI):
    app.add_exception_handler(InternalException, _internal_exception_handler)
    app.add_exception_handler(ApplicationException, _application_exception_handler)
    app.add_exception_handler(RequestValidationError, _fastapi_request_validation_error_handler)


def add_routers(app: FastAPI):
    app.include_router(connection_router)
    app.include_router(items_router)
    app.include_router(topics_router)
    app.include_router(users_router)


@asynccontextmanager
async def lifespan(_):
    init_db()
    yield
    shutdown_db()
