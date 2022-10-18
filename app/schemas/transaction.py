import uuid
import enum
from datetime import datetime
from pydantic import BaseModel
from typing import Union

from app.models.transaction import Status, TransactionType


# class TransactionType(str, enum.Enum):
#     desposit = "deposit"
#     withdrawal = "withdrawal"
#     transfer = "transfer"
    
# class Status(str,enum.Enum):
#     pending = "pending"
#     success = "success"
#     failed = "failed"

class TransactionResponse(BaseModel):
    id: uuid.UUID
    account_id: uuid.UUID
    user_id: uuid.UUID
    transaction_type: TransactionType
    status: Status
    amount: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
  