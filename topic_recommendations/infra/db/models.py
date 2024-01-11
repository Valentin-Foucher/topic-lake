from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from topic_recommendations.infra.db.core import Model


class User(Model):
    __tablename__ = 'users'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String, nullable=False)
    password = Column('password', String, nullable=False)

    topic_creations = relationship('Topic', back_populates='user', cascade='all, delete-orphan')
    item_creations = relationship('Item', back_populates='user', cascade='all, delete-orphan')


class Topic(Model):
    __tablename__ = 'topics'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id'))
    parent_id = mapped_column(ForeignKey('topics.id'))

    sub_topics = relationship('Topic', back_populates='parent_topic')
    parent_topic = relationship('Topic', remote_side=[id], back_populates='sub_topics')
    user = relationship('User', back_populates='topic_creations')
    item_creations = relationship('Item', back_populates='topic', cascade='all, delete-orphan')


class Item(Model):
    __tablename__ = 'items'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id'))
    topic_id = mapped_column(ForeignKey('topics.id'))

    user = relationship('User', back_populates='item_creations')
    topic = relationship('Topic', back_populates='item_creations')
