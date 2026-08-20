from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession 

from app.database import get_db 
from app.schemas.ticket import TicketCreate, TicketResponse 
from app.crud import ticket as crud_ticket


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket: TicketCreate,
    user_id: int = 1,
    db: AsyncSession = Depends(get_db),
):
    db_ticket = await crud_ticket.create_ticket(db, ticket, user_id)
    
    return db_ticket
