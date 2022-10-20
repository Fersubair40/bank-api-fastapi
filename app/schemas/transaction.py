import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Union, List

from app.models.transaction import Status, TransactionType
# from app.schemas.users import Pagination
# from app.utils.pagination import pagination



class TransactionBase(BaseModel):
    id: uuid.UUID
    account_id: uuid.UUID
    user_id: uuid.UUID
    transaction_type: TransactionType
    status: Status
    amount: int
    reference: Union[str, None] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True


class SingleTransaction(TransactionBase):
    pass

class TransactionResponse(BaseModel):
    transactions: List[TransactionBase]
    # pagination: Union[Pagination, None] = None