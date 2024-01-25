from dataclasses import dataclass


@dataclass
class Item:
    id: int
    content: str
    topic_content: str
    topic_id: int
    user_name: str
    user_id: int
    rank: int
