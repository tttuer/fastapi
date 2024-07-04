from pydantic import BaseModel


class Event(BaseModel):
    id: int
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
