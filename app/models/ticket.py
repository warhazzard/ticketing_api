from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from enum import Enum 
from sqlalchemy import func

from app.database import Base 


class TicketStatus(str, Enum):
    RESERVED = "reserved"
    PURCHASED = "purchased"
    EXPIRED = "expired"


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.RESERVED)
    created_at = Column(DateTime(timezone=True), default=func.now())