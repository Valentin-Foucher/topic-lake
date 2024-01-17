from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, mapped_column

from topic_recommendations.infra.db.core import Model


class User(Model):
    __tablename__ = 'users'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String, nullable=False)
    password = Column('password', String, nullable=False)

    topic_creations = relationship('Topic', back_populates='user', cascade='all, delete-orphan')
    item_creations = relationship('Item', back_populates='user', cascade='all, delete-orphan')
    access_tokens = relationship('AccessToken', back_populates='user', cascade='all, delete-orphan')


class Topic(Model):
    __tablename__ = 'topics'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    parent_topic_id = mapped_column(ForeignKey('topics.id'))

    sub_topics = relationship('Topic', back_populates='parent_topic', cascade='all, delete-orphan')
    parent_topic = relationship('Topic', remote_side=[id], back_populates='sub_topics')
    user = relationship('User', back_populates='topic_creations')
    item_creations = relationship('Item', back_populates='topic', cascade='all, delete-orphan')


class Item(Model):
    __tablename__ = 'items'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    topic_id = mapped_column(ForeignKey('topics.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='item_creations')
    topic = relationship('Topic', back_populates='item_creations')


class AccessToken(Model):
    __tablename__ = 'access_tokens'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    value = Column('content', String, nullable=False)
    creation_date = Column('creation_date', DateTime, default=datetime.utcnow)
    revoked = Column('revoked', Boolean, default=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='access_tokens')
