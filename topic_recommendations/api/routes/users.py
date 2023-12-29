from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.models.users import CreateUserModel
from topic_recommendations.app.controllers.users import UsersController
from topic_recommendations.infra.repositories.users import UsersRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_users(user: CreateUserModel):
    UsersController() \
        .with_repository(UsersRepository()) \
        .create(
            user.name,
            user.password
        )


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_topic(user_id: int):
    return UsersController() \
        .with_repository(UsersRepository()) \
        .get(user_id)