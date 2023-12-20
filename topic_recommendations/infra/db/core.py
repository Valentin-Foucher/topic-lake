import inspect
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from topic_recommendations import config

engine = create_engine(config.get('postgres.connection_string'))

session = scoped_session(sessionmaker(bind=engine))

Model = declarative_base(name='Model')
Model.query = session.query_property()
Model.as_dataclass = lambda s, clz: clz(**{c.name: getattr(s, c.name) for c in s.__table__.columns
                                           if c.name in inspect.signature(clz).parameters})

logger = logging.getLogger(__name__)


def init_db():
    logger.info('Initializing database')
    Model.metadata.create_all(engine)

