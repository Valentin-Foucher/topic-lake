import asyncio
from contextlib import ExitStack

import pytest
import pytest_asyncio

from topic_lake_api.api.utils.app_utils import init_app
from topic_lake_api.infra.db.core import sessionmanager, init_db


@pytest.fixture(scope='session', autouse=True)
def app():
    with ExitStack():
        yield init_app(testing=True)


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_manager(app, event_loop):
    init_db()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables(app, session_manager):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db(app, create_tables):
    async with sessionmanager.session() as db:
        try:
            await db.begin()
            yield db
        finally:
            await db.rollback()  # Rolls back the outer transaction
