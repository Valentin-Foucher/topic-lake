from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from topic_recommendations.infra.db.core import Model


class User(Model):
    __tablename__ = 'users'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String, nullable=False)
    password = Column('password', String, nullable=False)

    topic_creations: Mapped['Topic'] = relationship(back_populates='created_by', cascade='all, delete-orphan')
    item_creations: Mapped['Item'] = relationship(back_populates='created_by', cascade='all, delete-orphan')


class Topic(Model):
    __tablename__ = 'topics'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id'))

    created_by: Mapped['User'] = relationship(back_populates='topic_creations')
    item_creations: Mapped['Item'] = relationship(back_populates='related_topic', cascade='all, delete-orphan')


class Item(Model):
    __tablename__ = 'items'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    content = Column('content', String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id'))
    topic_id = mapped_column(ForeignKey('topics.id'))

    created_by: Mapped['User'] = relationship(back_populates='item_creations')
    related_topic: Mapped['Topic'] = relationship(back_populates='item_creations')
