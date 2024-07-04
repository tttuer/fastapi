from typing import List

from fastapi import APIRouter, HTTPException, status

from planner.models.events import Event

event_router = APIRouter(
    tags=["Event"],
)

events = []


@event_router.get("/", response_model=List[Event])
async def get_events() -> List[Event]:
    return events


@event_router.get("/{id}", response_model=Event)
async def get_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found",
    )


@event_router.post("/", response_model=Event)
async def create_event(event: Event) -> Event:
    events.append(event)
    return event


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {
                'message': 'Event deleted',
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found",
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        'message': 'All event deleted',
    }
