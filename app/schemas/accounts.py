from typing import List
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Union

from app.schemas.transaction import TransactionBase
# from app.schemas import users


class AccountBase(BaseModel):
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class CreateAccount(BaseModel):
    active: bool = False


# class UserBase(BaseModel):
#     name: str
#     email: str
#     photo: str
#
#     class Config:
#         orm_mode = True
#
# class UserResponse(UserBase):
#     id: uuid.UUID
#     created_at: datetime
#     updated_at: datetime
#     verified: bool = False


class UserAccountResponse(AccountBase):
    id: uuid.UUID
    available_balance: float
    active: bool = False
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    # transactions: List[TransactionResponse] = []


class Withdraw(BaseModel):
    amount: int
    
class DepositResponse(BaseModel):
    message: str
    account: UserAccountResponse
    transaction: TransactionBase
   
    
    
class Transfer(BaseModel):
    amount: int
    destination: str