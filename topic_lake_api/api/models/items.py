from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    content: str
    topic_content: str
    user_name: str
    rank: int


class CreateItemRequest(BaseModel):
    content: str = Field(min_length=4, max_length=256)
    rank: int = Field(gt=0, default=1_000_000)


class GetItemResponse(BaseModel):
    item: Item


class ListItemsResponse(BaseModel):
    items: list[Item]


class UpdateItemRequest(BaseModel):
    content: str = Field(min_length=4, max_length=256)
    rank: int
