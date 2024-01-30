from functools import wraps

from topic_lake_api.infra.db.core import get_session


def with_another_user(name='other_user', password='password123', admin=False):
    def decorator(f):
        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            u = self._create_test_user(name=name, password=password, admin=admin)
            with get_session() as session:
                session.add(u)
                session.flush()
                session.commit()

                self.other_user_id = u.id

            result = await f(self, *args, **kwargs)

            self.other_user_id = None
            with get_session() as session:
                session.delete(u)
                session.commit()

            return result

        return wrapper

    return decorator
