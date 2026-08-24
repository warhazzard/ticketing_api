from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession 

from app.database import get_db 
from app.schemas.ticket import TicketCreate, TicketResponse 
from app.crud import ticket as crud_ticket
from app.dependencies import get_current_user
from app.models import User


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = await crud_ticket.create_ticket(db, ticket, current_user.id)
    
    return db_ticket

