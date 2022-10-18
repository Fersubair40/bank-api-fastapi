import base64
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status

from ..config import settings
from ..database import get_db
from ..models import users
from sqlalchemy.orm import Session


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()


class UserNotFound(Exception):
    pass


def current_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = db.query(users.User).filter(users.User.id == user_id).first()
    if not user:
        raise UserNotFound("User not found")
    return user_id
