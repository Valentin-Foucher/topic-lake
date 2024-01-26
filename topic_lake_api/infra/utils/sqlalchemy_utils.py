from functools import wraps

from sqlalchemy.orm import Relationship


def with_join_depth(relationship: Relationship, depth: int):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            original_join_depth = relationship.property.strategy.join_depth
            relationship.property.strategy.join_depth = depth

            result = await f(*args, **kwargs)

            relationship.property.strategy.join_depth = original_join_depth

            return result

        return wrapper
    return decorator
