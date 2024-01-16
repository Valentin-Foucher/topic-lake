from topic_recommendations.interactor.interfaces.base import Presenter


class LogInPresenter(Presenter):
    def present(self, token_value: str):
        return {'token': token_value}
