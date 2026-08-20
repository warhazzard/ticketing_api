from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.event import Event
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate 


async def create_ticket(db: AsyncSession, ticket: TicketCreate, user_id: int):
    query = select(Event).where(Event.id == ticket.event_id).with_for_update()
    result = await db.execute(query)
    event_obj = result.scalar_one_or_none()

    if event_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event_obj.available_tickets <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tickets available")
    
    event_obj.available_tickets -= 1
    
    db_ticket = Ticket(**ticket.model_dump(), user_id=user_id)
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)

    return db_ticket

