from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from pydantic import EmailStr
from app.utils import hash_password
from ..schemas.users import CreateUserResponse, CreateUser, LoginResponse, LoginUser
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..database import get_db
from app.utils.jwt import AuthJWT
from ..config import settings
from ..models import users

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post("/register", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: CreateUser, db: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends()):
    user = db.query(users.User).filter(users.User.email == EmailStr(payload.email.lower())).first()
    if user:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"message": "User already exists"})
    if payload.password != payload.password_confirm:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Passwords do not match"})

    payload.password = hash_password.hash_password(payload.password)
    del payload.password_confirm
    payload.verified = True
    payload.email = EmailStr(payload.email.lower())
    new_user = users.User(**payload.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = Authorize.create_access_token(
        subject=str(new_user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(
        subject=str(new_user.id), expires_time=timedelta(days=REFRESH_TOKEN_EXPIRES_IN))
    return {"user": new_user, "access_token": access_token, "refresh_token": refresh_token}


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginUser,
                db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = db.query(users.User).filter(users.User.email == EmailStr(payload.email.lower())).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"message": "Invalid credentials"})

    if not hash_password.verify_password(payload.password, user.password):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"message": "Invalid credentials"})
    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(days=REFRESH_TOKEN_EXPIRES_IN))
    return {"access_token": access_token, "refresh_token": refresh_token, "user": user}
