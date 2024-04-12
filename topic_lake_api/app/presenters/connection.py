from topic_lake_api.domain.interfaces.base import Presenter


class LogInPresenter(Presenter):
    def present(self, token_value: str, user_id: int):
        return {
            'token': token_value,
            'user_id': user_id
        }
