from pydantic import BaseModel


class CreateItemModel(BaseModel):
    content: str
    topic_id: int
    user_id: int
