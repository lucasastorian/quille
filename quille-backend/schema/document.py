from typing import TypedDict


class Document(TypedDict):
    id: str
    name: str
    content: str
    created_at: str
    updated_at: str
