from topic_recommendations.app.presenters.base import Presenter
from topic_recommendations.interactor.dtos.outputs.items import ListItemsOutputDto, GetItemOutputDto


class ListItemsPresenter(Presenter):
    def present(self, output_dto: ListItemsOutputDto):
        return {'items': None}


class GetItemPresenter(Presenter):
    def present(self, output_dto: GetItemOutputDto):
        return {'item': None}
