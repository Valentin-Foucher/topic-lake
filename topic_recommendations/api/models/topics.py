from pydantic import BaseModel


class CreateTopicRequest(BaseModel):
    content: str
    user_id: int


class Topic(BaseModel):
    id: int
    content: str
    user_id: int


class GetTopicResponse(BaseModel):
    topic: Topic


class ListTopicsResponse(BaseModel):
    topics: list[Topic]
