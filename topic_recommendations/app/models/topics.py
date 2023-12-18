from pydantic import BaseModel


class CreateTopicModel(BaseModel):
    content: str
    user_id: int
