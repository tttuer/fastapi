from typing import Optional, List

from beanie import Document


class Event(Document):
    title: str
    image: str
    description: str
    tags: list[str]
    location: str

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

    class Settings:
        name = 'events'


class EventUpdate(Document):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

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
