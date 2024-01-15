import inspect
import logging
import re
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
    previously_looked_up_models = []

    def as_dataclass_(model_: Model | list[Model]):
        nonlocal previously_looked_up_models

        if isinstance(model_, list):
            return [as_dataclass_(sub) for sub in model_]

        previously_looked_up_models.append(str(model_.__class__))
        clz = get_object_by_name(f'topic_recommendations.domain.entities.{model_.__class__.__name__}')
        dataclass_attributes = inspect.signature(clz).parameters
        kwargs = {}

        for c in model_.__table__.columns:
            if c.name in dataclass_attributes:
                kwargs[c.name] = getattr(model_, c.name)

        for m in model_.__mapper__.relationships:
            if m.argument in previously_looked_up_models:
                continue

            sub_model_value = getattr(model_, m.key)
            if not sub_model_value:
                continue

            # storing nesting object attribute as nested dataclass
            if any(p == m.key and sub_model_value for p in dataclass_attributes):
                kwargs[m.key] = as_dataclass_(sub_model_value)

            # storing nesting object attribute as simple parent attribute
            else:
                prefix = f'{m.key}_'
                for complete_name in dataclass_attributes:
                    if complete_name.startswith(prefix) and complete_name in dataclass_attributes:
                        kwargs[complete_name] = getattr(sub_model_value, re.sub(prefix, '', complete_name))

        return clz(**kwargs)

    return as_dataclass_(model)


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
