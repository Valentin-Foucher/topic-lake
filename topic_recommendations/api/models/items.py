from pydantic import BaseModel


class CreateItemModel(BaseModel):
    content: str
    user_id: int


class Item(BaseModel):
    id: int
    content: str
    topic: str
    user_name: str


class GetItem(BaseModel):
    item: Item


class ListItems(BaseModel):
    items: list[Item]
