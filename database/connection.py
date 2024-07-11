from typing import Optional, Any, List

from beanie import init_beanie, PydanticObjectId, Document
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from planner.models.events import Event
from planner.models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None

    async def init_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), document_models=[Event, User])

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model: Event | User):
        self.model = model

    async def save(self, document: Document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Document | bool:
        doc = await self.model.get(document_id=id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Document | bool:
        doc_id = id
        des_body = body.model_dump()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc: Document = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc: Document = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
