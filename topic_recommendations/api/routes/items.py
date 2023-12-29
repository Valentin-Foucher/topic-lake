from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.models.items import CreateItemModel
from topic_recommendations.app.controllers.items import ItemsController
from topic_recommendations.infra.repositories.items import ItemsRepository

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get('/', status_code=status.HTTP_200_OK)
async def list_items():
    return ItemsController() \
        .with_repository(ItemsRepository()) \
        .list()


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def create_item(item: CreateItemModel):
    ItemsController() \
        .with_repository(ItemsRepository()) \
        .create(
            item.user_id,
            item.topic_id,
            item.content
        )


@router.get('/{item_id}', status_code=status.HTTP_200_OK)
async def get_item(item_id: int):
    return ItemsController() \
        .with_repository(ItemsRepository()) \
        .get(item_id)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    ItemsController() \
        .with_repository(ItemsRepository()) \
        .delete(item_id)
