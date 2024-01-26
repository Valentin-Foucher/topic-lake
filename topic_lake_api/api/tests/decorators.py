from functools import wraps

from topic_lake_api.infra.db.core import sessionmanager


def with_another_user(name='other_user', password='password123', admin=False):
    def decorator(f):
        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            async with sessionmanager.session() as db:
                u = await self.create_test_user(db, name=name, password=password, admin=admin)
                self.other_user_id = u.id

                result = await f(self, *args, **kwargs)

                self.other_user_id = None
                db.delete(u)
                db.commit()

            return result

        return wrapper

    return decorator
