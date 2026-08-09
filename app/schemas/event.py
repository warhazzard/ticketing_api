from pydantic import BaseModel, Field, ConfigDict 
from datetime import datetime 

from app.models.user import UserRole 


class EventCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Name of the event")
    date: datetime = Field(description="Date and time of the event")
    total_tickets: int = Field(gt=0, description="Total number of tickets available")
    available_tickets: int = Field(description="Number of available tickets")


class EventResponse(EventCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="Unique identifier of the event")
    