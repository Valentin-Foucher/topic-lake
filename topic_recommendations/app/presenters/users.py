import dataclasses

from topic_recommendations.app.presenters.base import Presenter
from topic_recommendations.interactor.dtos.outputs.users import GetUserOutputDto


class GetUserPresenter(Presenter):
    def present(self, output_dto: GetUserOutputDto):
        return {'user': dataclasses.asdict(output_dto.user)}
