import enum
import uuid
from app.exceptions.exceptio import InsuffiiantAmount, MaxAmount
from .model import Base
from sqlalchemy import Column, TIMESTAMP, String, DECIMAL, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID


class TransactionType(enum.Enum):
    desposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"
    
class Status(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey(
        'accounts.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(Status), nullable=False, default='pending')
    
    amount = Column(DECIMAL, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    
    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    

   