from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import HTTPException, status 
from sqlalchemy import select 

from app.models.user import User 
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_hashed_password


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user