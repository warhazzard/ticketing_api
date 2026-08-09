from pydantic import BaseModel, Field, ConfigDict 
from datetime import datetime 

from app.models.ticket import TicketStatus  

class TicketCreate(BaseModel):
    event_id: int = Field(description="Unique identifier of the event")


class TicketResponse(TicketCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="Unique identifier of the ticket")
    user_id: int = Field(description="Unique identifier of the user")
    status: TicketStatus = Field(default=TicketStatus.RESERVED, description="Status of the ticket")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of ticket purchase")

