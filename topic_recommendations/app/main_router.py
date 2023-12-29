from fastapi import APIRouter, status

from topic_recommendations.api.routes import router as items_router
from topic_recommendations.api.routes.topics import router as topics_router
from topic_recommendations.api.routes.users import router as users_router

router = APIRouter(
    prefix="/api/v1",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

router.include_router(items_router)
router.include_router(topics_router)
router.include_router(users_router)
