from dataclasses import dataclass
from typing import Optional


@dataclass
class Topic:
    id: int
    content: str
    user_id: int
    parent_topic_id: Optional[int] = None
