from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from enum import Enum 

from app.database import Base 


class UserRole(str, Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.CUSTOMER)
