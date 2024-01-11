import inspect
import logging
from typing import Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from topic_recommendations import config

engine = create_engine(config.get('postgres.connection_string'))

session = scoped_session(sessionmaker(bind=engine))

Model = declarative_base(name='Model')
TModel = TypeVar("TModel", bound=Model)

Model.query = session.query_property()


def as_dataclass(model: Model, clz: Type[TModel]):
    dataclass_kwargs = {}
    dataclass_attributes = inspect.signature(clz).parameters
    previously_looked_up_models = []

    def flatten_model(sub_model: Model, prefix: str = ''):
        nonlocal dataclass_kwargs, dataclass_attributes, previously_looked_up_models

        if sub_model is None or isinstance(sub_model, list):
            return

        for c in sub_model.__table__.columns:
            complete_name = prefix + c.name
            if complete_name in dataclass_attributes:
                dataclass_kwargs[complete_name] = getattr(sub_model, c.name)

        for m in sub_model.__mapper__.relationships:
            if m.key in previously_looked_up_models:
                continue

            previously_looked_up_models.append(m.key)
            prefix = f'{m.argument.lower()}_'
            if any(p.startswith(prefix) for p in dataclass_attributes):
                flatten_model(
                    getattr(sub_model, m.key),
                    prefix=prefix
                )

    flatten_model(model)
    return clz(**dataclass_kwargs)


Model.as_dataclass = as_dataclass

logger = logging.getLogger(__name__)


def init_db():
    logger.info('Initializing database')
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        engine.connect()

    Model.metadata.create_all(engine)


def shutdown_db():
    logger.info('Shutting down database connection')
    engine.dispose()
