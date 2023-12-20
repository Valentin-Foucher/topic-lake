from dataclasses import dataclass

from topic_recommendations.domain.entities.users import User
from topic_recommendations.interactor.dtos.outputs.base import OutputDto


@dataclass
class GetUserOutputDto(OutputDto):
    user: User
