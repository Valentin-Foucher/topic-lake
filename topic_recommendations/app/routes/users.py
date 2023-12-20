from fastapi import APIRouter
from starlette import status

from topic_recommendations.app.models.users import CreateUserModel
from topic_recommendations.app.views.users import UsersView
from topic_recommendations.infra.repositories.users import UsersRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
view = UsersView(UsersRepository())


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_users(user: CreateUserModel):
    view.create(user.name, user.password)


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_topic(user_id: int):
    return view.get(user_id)
