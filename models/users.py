from typing import Optional, List

from beanie import Document
from pydantic import BaseModel, EmailStr

from planner.models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = None

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'ex.example.com',
                'events': [],
            }
        }

    class Settings:
        name = 'users'


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
