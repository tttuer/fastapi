from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from planner.database.connection import Database
from planner.models.events import Event

event_router = APIRouter(
    tags=["Event"],
)

events = []

event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def get_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def get_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found",
    )


@event_router.post("/")
async def create_event(event: Event) -> dict:
    await event_database.save(event)
    return {
        'message': 'event created successfully',
    }


@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, event: Event) -> Event:
    updated_event = await event_database.update(id, event)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return {
        'message': 'Event deleted',
    }


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        'message': 'All event deleted',
    }
