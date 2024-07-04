from typing import List, Optional

from sqlmodel import SQLModel, Field, JSON, Column


class Event(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            'example': {
                'title': 'ex title',
                'description': 'ex description',
                'location': 'ex location',
                'tags': ['tag1', 'tag2'],
                'image': 'ex image'
            }
        }


class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    location: Optional[str] = None

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'ex title',
                'description': 'ex description',
                'location': 'ex location',
                'tags': ['tag1', 'tag2'],
                'image': 'ex image'
            }
        }
