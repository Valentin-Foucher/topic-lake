import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.dependencies.utils import get_dependant
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from topic_lake_api.api.routes.connection import router as connection_router
from topic_lake_api.api.routes.items import router as items_router
from topic_lake_api.api.routes.topics import router as topics_router
from topic_lake_api.api.routes.users import router as users_router
from topic_lake_api.api.utils.exception_utils import status_code_from_application_exception
from topic_lake_api.api.utils.route_utils import inject_scoped_session_in_repositories
from topic_lake_api.domain.exceptions import ApplicationException
from topic_lake_api.exceptions import InternalException
from topic_lake_api.infra.db.core import init_db, shutdown_db

logger = logging.getLogger(__name__)


def _db_error_handler(_, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
        'detail': 'Internal Server Error'
    })


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
        'detail': [{
            'message': err['msg'],
            'field': err['loc'][-1],
            'value': err['input'].decode('utf-8') if isinstance(err['input'], bytes) else err['input']
        } for err in exc.errors()]
    })


def _add_error_handlers(app: FastAPI):
    app.add_exception_handler(SQLAlchemyError, _db_error_handler)
    app.add_exception_handler(InternalException, _internal_exception_handler)
    app.add_exception_handler(ApplicationException, _application_exception_handler)
    app.add_exception_handler(RequestValidationError, _fastapi_request_validation_error_handler)


def _add_routers(app: FastAPI, api_version: int):
    match api_version:
        case 1:
            _add_v1_router(app)
        case _:
            raise InternalException('Invalid API version')


def _add_v1_router(app: FastAPI):
    main_router = APIRouter(prefix='/api/v1')
    main_router.include_router(connection_router)
    main_router.include_router(items_router)
    main_router.include_router(topics_router)
    main_router.include_router(users_router)
    for route in main_router.routes:
        route.endpoint = inject_scoped_session_in_repositories(route.endpoint)
        route.dependant = get_dependant(path=route.path_format, call=route.endpoint)

    app.include_router(main_router)


def _add_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_):
        init_db()
        yield
        shutdown_db()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    _add_routers(app, api_version=1)
    _add_error_handlers(app)
    return app
