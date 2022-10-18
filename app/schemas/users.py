import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from app.schemas import accounts
from typing import List, Union


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    photo: str

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: constr(min_length=6)
    password_confirm: constr(min_length=6)
    verified: bool = False


class LoginUser(BaseModel):
    password: constr(min_length=6)
    email: EmailStr


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    verified: bool = False
    


class SingleUser(UserResponse):

    account: Union[accounts.UserAccountResponse, None] = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse


class CreateUserResponse(LoginResponse):
    pass

class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    # email: Union[EmailStr, None] = None
    # photo: Union[str, None] = None
    # mobile: Union[str, None] = None


class Pagination(BaseModel):
    total: int
    limit: int
    page: int
    prev: Union[int, None] = None
    next: Union[int, None] = None


class PaginationUserSchema(BaseModel):
    users: List[UserResponse]
   
    pagination: Union[Pagination, None] = None