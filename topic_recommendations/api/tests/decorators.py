from functools import wraps

from topic_recommendations.infra.db.core import session


def with_another_user(name='other_user', password='password123'):
    def decorator(f):
        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            u = self._create_test_user(name=name, password=password)
            self.other_user_id = u.id

            result = await f(self, *args, **kwargs)

            self.other_user_id = None
            session.delete(u)
            session.commit()
            return result

        return wrapper

    return decorator
