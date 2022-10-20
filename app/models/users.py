import datetime
from email.policy import default

from typing import Dict
from curses.ascii import US
import uuid

from app.schemas.users import UpdateUser
from .model import Base
from sqlalchemy import Column, String, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func
from ..database import get_db
from fastapi import Depends

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    verified = Column(Boolean, nullable=False, server_default="false")
    mobile = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)

    account = relationship("Account", uselist=False, backref='user')
    
    transactions = relationship("Transaction")



    def search(params: Dict[str, str],  db: Session):
       
        users = db.query(User).order_by(User.created_at.desc()).limit(params["limit"]).offset(params["offset"]).all()
        
        users = db.query(User).filter_by(first_name = params['name'])\
            .order_by(User.created_at.desc())\
            .limit(params["limit"]).offset(params["offset"])\
            .all() if params['name'] else users
        users = db.query(User).filter_by(email = params['email'])\
             .order_by(User.created_at.desc())\
             .limit(params["limit"]).offset(params["offset"])\
             .all() if params['email'] else users
        
        return users
        
    
    
    def update(self, payload: UpdateUser):
        self.first_name = payload.first_name
        self.last_name = payload.last_name
        return self
    
    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
        
    # def withdraw(self, amount):
    #     if self.account.available_balance >= amount:
    #         self.account.available_balance -= amount
    #         return True
    #     return False
