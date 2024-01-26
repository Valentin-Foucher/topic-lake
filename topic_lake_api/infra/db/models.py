from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column

from topic_lake_api.infra.db.core import Model


class User(Model):
    __tablename__ = 'users'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    admin = Column('admin', Boolean, default=False)

    topic_creations = relationship('Topic', back_populates='user', lazy='selectin', cascade='all, delete-orphan')
    item_creations = relationship('Item', back_populates='user', lazy='selectin', cascade='all, delete-orphan')
    access_tokens = relationship('AccessToken', back_populates='user', lazy='selectin', cascade='all, delete-orphan')


class Topic(Model):
    __tablename__ = 'topics'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    parent_topic_id = mapped_column(ForeignKey('topics.id', ondelete='CASCADE'))

    sub_topics = relationship('Topic', back_populates='parent_topic', lazy='joined', join_depth=10,
                              cascade='all, delete-orphan')
    parent_topic = relationship('Topic', remote_side=[id], lazy='joined', join_depth=1,
                                back_populates='sub_topics')
    user = relationship('User', lazy='joined', join_depth=1, back_populates='topic_creations')
    item_creations = relationship('Item', back_populates='topic', lazy='selectin', cascade='all, delete-orphan')

    __table_args__ = (UniqueConstraint('content', 'parent_topic_id'),)


class Item(Model):
    __tablename__ = 'items'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    rank = Column('rank', Integer, nullable=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    topic_id = mapped_column(ForeignKey('topics.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='item_creations', lazy='selectin')
    topic = relationship('Topic', back_populates='item_creations', lazy='selectin')

    __table_args__ = (UniqueConstraint('topic_id', 'rank', deferrable=True),)


class AccessToken(Model):
    __tablename__ = 'access_tokens'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    value = Column('content', String, nullable=False)
    creation_date = Column('creation_date', DateTime, default=datetime.utcnow)
    revoked = Column('revoked', Boolean, default=False)
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='access_tokens', lazy='selectin')
