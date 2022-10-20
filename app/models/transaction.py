import datetime
from email.policy import default
import enum
from typing import Dict
import uuid
from app.exceptions.exceptio import InsuffiiantAmount, MaxAmount
from .model import Base
from sqlalchemy import Column, TIMESTAMP, String, DECIMAL, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


class TransactionType(enum.Enum):
    deposit = "deposit"
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
    reference = Column(String(255), nullable=True)
    
    amount = Column(DECIMAL, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    
    
    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    

    def search(param: Dict[str, str], db: Session, user_id: str):
        transactions = db.query(Transaction).order_by(Transaction.created_at.desc())\
            .filter(Transaction.user_id == user_id)\
            .limit(param["limit"]).offset(param["offset"])\
            .all() 
        
        transactions = db.query(Transaction).order_by(Transaction.created_at.desc())\
            .filter(Transaction.amount == param["amount"])\
            .limit(param["limit"]).offset(param["offset"])\
            .all() if param["amount"] else transactions
        
        transactions = db.query(Transaction)\
            .filter(Transaction.transaction_type == param["transaction_type"])\
            .limit(param["limit"]).offset(param["offset"])\
            .all() if param["transaction_type"] else transactions
            
        transactions = db.query(Transaction)\
            .filter(Transaction.status == param["status"])\
             .limit(param["limit"]).offset(param["offset"])\
            .all() if param["status"] else transactions
        return transactions
   