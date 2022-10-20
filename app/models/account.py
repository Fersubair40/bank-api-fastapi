# from http.client import HTTPException
import datetime
from email.policy import default
import uuid
from app.exceptions.exceptio import InsuffiiantAmount, MaxAmount
from .model import Base
from sqlalchemy import Column, TIMESTAMP, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from sqlalchemy.sql import func


class Account(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    available_balance = Column(DECIMAL, nullable=False, default=0)
    active = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    
    transactions = relationship("Transaction", uselist=True)
    
    
    def withdraw(self, amount):
        if amount > self.available_balance or amount == 0:
            raise InsuffiiantAmount('Insufficient amount')
        else:
            self.available_balance -= amount
            return self
    
    def deposit(self, amount):
        if amount > 50000:
            raise MaxAmount("you can't deposit more than 50,000")
        else:
            self.available_balance += amount
            return self
        
        
    def transfer(self, amount, destination):
        if amount > self.available_balance or amount == 0:
            raise InsuffiiantAmount('Insufficient amount')
        else:
            self.withdraw(amount=amount)
            destination.deposit(amount)
            return self

      
    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
        

    
