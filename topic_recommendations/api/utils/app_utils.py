import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from topic_recommendations.api.routes.items import router as items_router
from topic_recommendations.api.routes.topics import router as topics_router
from topic_recommendations.api.routes.users import router as users_router
from topic_recommendations.exceptions import InternalException
from topic_recommendations.infra.db.core import init_db

logger = logging.getLogger(__name__)


def _internal_exception_handler(request: Request, exc: InternalException) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content='')


def add_error_handlers(app: FastAPI):
    app.add_exception_handler(InternalException, _internal_exception_handler)


def add_routers(app: FastAPI):
    app.include_router(items_router)
    app.include_router(topics_router)
    app.include_router(users_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
