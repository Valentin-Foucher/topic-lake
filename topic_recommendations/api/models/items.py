from pydantic import BaseModel


class Item(BaseModel):
    id: int
    content: str
    topic_content: str
    user_name: str


class CreateItemRequest(BaseModel):
    content: str
    user_id: int


class GetItemResponse(BaseModel):
    item: Item


class ListItemsResponse(BaseModel):
    items: list[Item]
