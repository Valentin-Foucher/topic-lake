from dataclasses import dataclass


@dataclass
class Item:
    id: int
    content: str
    topic_content: str
    user_name: str
    rank: int
