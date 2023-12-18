from dataclasses import dataclass


@dataclass
class Item:
    id: int
    content: str
    topic: str
    user_name: str
