from topic_recommendations.app.utils.data_utils import SingletonMeta


class Controller(metaclass=SingletonMeta):
    """
    The controller is a design pattern which aim is to take the input it is given and to convert it into
    the form required by the business.
    In this implementation, it is responsible for creating the response content, but it can be delegated by using a
    presenter.
    """
    pass
