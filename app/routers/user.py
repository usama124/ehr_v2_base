from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_password_hash, verify_password, create_access_token
from app.core.database import get_db
from app.core.dependency import get_current_user
from app.core.responses import BadRequestException, UnauthorizedException, ApiCustomResponse
from app.crud import user_crud, role_perm_crud
from app.schema import UserCreate, UserLogin

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await user_crud.check_user_exists_by_email(db, user.email.__str__())
    if existing_user:
        raise BadRequestException(message="Email already registered")

    role = await role_perm_crud.get_role_by_name(db=db, role=user.role.value)
    if role is None:
        raise BadRequestException(message="Invalid role provided.")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = await user_crud.create_user(db, role_id=role.id, user_create=user)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=new_user)


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_email(db, user.email.__str__())
    if not db_user or not verify_password(user.password, db_user.password):
        raise UnauthorizedException(message="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    user_response = await user_crud.construct_user_serialized_response(db_user)
    response = {"access_token": token, "user": user_response}
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.get("/me")
async def get_me(
        user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_obj = await user_crud.get_user_by_email(db=db, email=user.email)
    response = await user_crud.construct_user_serialized_response(user_obj)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)
