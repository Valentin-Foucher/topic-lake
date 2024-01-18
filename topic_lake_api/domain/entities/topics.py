from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Topic:
    id: int
    content: str
    user_id: int
    parent_topic_id: Optional[int] = None
    sub_topics: list['Topic'] = field(default_factory=list)
