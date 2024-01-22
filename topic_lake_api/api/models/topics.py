from typing import Optional

from pydantic import BaseModel


class Topic(BaseModel):
    id: int
    content: str
    user_id: int
    parent_topic_id: Optional[int] = None
    sub_topics: Optional[list['Topic']] = None


class CreateTopicRequest(BaseModel):
    content: str
    parent_topic_id: Optional[int] = None


class CreateTopicResponse(BaseModel):
    id: int


class GetTopicResponse(BaseModel):
    topic: Topic


class ListTopicsResponse(BaseModel):
    topics: list[Topic]
