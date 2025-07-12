from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import decode_token
from app.core.database import get_db
from app.core.responses import UnauthorizedException, TokenExpired
from app.crud.user import get_user_by_email

bearer_scheme = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db),
):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException(message="Could not validate credentials")
    except ExpiredSignatureError:
        raise TokenExpired()
    except JWTError:
        raise UnauthorizedException(message="Could not validate credentials")

    user = await get_user_by_email(db=db, email=email)
    if user is None:
        raise UnauthorizedException(message="Could not validate credentials")
    return user
