from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt 

from .core.security import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_email
from app.schemas.user import TokenData
from app.database import get_db 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])    
        email: str = payload.get("sub")
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credential_exception
    
    user = await get_user_by_email(db, token_data.email)
    if user is None:
        raise credential_exception
    
    return user