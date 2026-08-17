from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.crud import event as crud_event


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventResponse)
async def create_new_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    db_event = await crud_event.create_event(db, event)
    return db_event 
    

