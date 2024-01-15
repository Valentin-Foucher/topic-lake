import inspect
import logging
from typing import TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from topic_recommendations import config
from topic_recommendations.utils.object_utils import get_object_by_name

engine = create_engine(config.get('postgres.connection_string'))

session = scoped_session(sessionmaker(bind=engine))

Model = declarative_base(name='Model')
TModel = TypeVar("TModel", bound=Model)

Model.query = session.query_property()


def as_dataclass(model: Model | list[Model]):
    clz = get_object_by_name(f'topic_recommendations.domain.entities.{model.__class__.__name__}')
    dataclass_kwargs = {}
    dataclass_attributes = inspect.signature(clz).parameters
    previously_looked_up_models = []

    def flatten_model(sub_model: Model | list[Model] | None, prefix: str = ''):
        nonlocal dataclass_kwargs, dataclass_attributes, previously_looked_up_models

        if sub_model is None:
            return
        if isinstance(sub_model, list):
            for sub in sub_model:
                flatten_model(sub)

        for c in sub_model.__table__.columns:
            complete_name = prefix + c.name
            if complete_name in dataclass_attributes:
                dataclass_kwargs[complete_name] = getattr(sub_model, c.name)

        for m in sub_model.__mapper__.relationships:
            if m.key in previously_looked_up_models:
                continue

            previously_looked_up_models.append(m.key)
            prefix = f'{m.key}_'
            sub_model_value = getattr(sub_model, m.key)
            if any(p == m.key and sub_model_value for p in dataclass_attributes):
                dataclass_kwargs[m.key] = as_dataclass(sub_model_value)
            elif any(p.startswith(prefix) for p in dataclass_attributes):
                flatten_model(sub_model_value, prefix=prefix)

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
