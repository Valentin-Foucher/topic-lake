import contextlib
import inspect
import logging
import re
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from topic_lake_api import config
from topic_lake_api.utils.object_utils import get_object_by_name

logger = logging.getLogger(__name__)


Model = declarative_base(name='Model')


class DatabaseSessionManager:
    def __init__(self):
        self.host = None
        self._engine = None
        self._session_maker = None

    def init(self, host: str):
        self.host = host
        self._engine = create_async_engine(host)
        self._session_maker = async_sessionmaker(autocommit=False, expire_on_commit=False, bind=self._engine)

    def is_initialized(self) -> bool:
        return self._engine is not None

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Model.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Model.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session


def as_dataclass(model: Model | list[Model], with_sub_children: bool = False, sub_relationship: bool = False):
    if isinstance(model, list):
        if sub_relationship and not with_sub_children:
            return None
        return [as_dataclass(sub, with_sub_children=with_sub_children, sub_relationship=True) for sub in model]

    clz = get_object_by_name(f'topic_lake_api.domain.entities.{model.__class__.__name__}')
    dataclass_attributes = inspect.signature(clz).parameters
    kwargs = {}

    for c in model.__table__.columns:
        if c.name in dataclass_attributes:
            kwargs[c.name] = getattr(model, c.name)

    for m in model.__mapper__.relationships:
        sub_model_value = getattr(model, m.key)
        if not sub_model_value:
            continue

        # storing nesting object attribute as nested dataclass
        if any(p == m.key and sub_model_value for p in dataclass_attributes):
            kwargs[m.key] = as_dataclass(sub_model_value, with_sub_children=with_sub_children)

        # storing nesting object attribute as simple parent attribute
        else:
            prefix = f'{m.key}_'
            for complete_name in dataclass_attributes:
                if complete_name.startswith(prefix) and complete_name in dataclass_attributes:
                    kwargs[complete_name] = getattr(sub_model_value, re.sub(prefix, '', complete_name))

    return clz(**kwargs)


Model.as_dataclass = as_dataclass


def init_db():
    logger.info('Initializing database')
    sessionmanager.init(config.get('postgres.connection_string'))


async def shutdown_db():
    logger.info('Shutting down database connection')
    if sessionmanager.is_initialized():
        await sessionmanager.close()
