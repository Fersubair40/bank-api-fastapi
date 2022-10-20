from datetime import datetime
from typing import List
import secrets

from app.exceptions.exceptio import InsuffiiantAmount, MaxAmount
from ..schemas import accounts
from ..models import account, transaction
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, status
from ..database import get_db
from ..utils.jwt import  current_user
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=accounts.UserAccountResponse, operation_id="jwt_required")
def create_account(user_account: accounts.CreateAccount, db: Session = Depends(get_db),
                   owner_id: str = Depends(current_user)):
    user_has_account = db.query(account.Account).filter_by(user_id=owner_id).first()
    if user_has_account:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"message": "account generated"})
    # user_account.user_id = uuid.UUID(owner_id)
    user_account.active = True
    new_account = account.Account(user_id=owner_id ,**user_account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


@router.post("/withdraw", response_model=accounts.DepositResponse,  status_code=status.HTTP_200_OK, operation_id="jwt_optional")
def withdraw(user_account: accounts.Withdraw, db: Session = Depends(get_db),
             owner_id: str = Depends(current_user)):
    get_account = db.query(account.Account).filter_by(user_id=owner_id).first()
    try:
        get_account.withdraw(user_account.amount)
        get_account.save(db)
        get_account.transactions.append(transaction.Transaction(
            amount=user_account.amount,
            user_id=owner_id,
            # account_id=get_account.id,
            status="success",
            transaction_type="withdrawal",
            reference=secrets.token_hex(16).upper()
            
        ))
        db.commit()
        # trxn.save(db)
        
    except Exception as e:
        
        return JSONResponse(status_code=403,
                        content={"message": str(e)}
                        )
   
    return {"message": "Withdrawal success", "account": get_account}


@router.post("/deposit", response_model=accounts.DepositResponse,  status_code=status.HTTP_200_OK, operation_id="fresh_jwt_required")
def deposit(user_account: accounts.Withdraw, db: Session = Depends(get_db),
             owner_id: str = Depends(current_user)):
    get_account = db.query(account.Account).filter_by(user_id=owner_id).first()
    
    try:
        get_account.deposit(user_account.amount)
     
        trxn = transaction.Transaction(
            amount=user_account.amount,
            user_id=owner_id,
            account_id=get_account.id,
            status="success",
            transaction_type="deposit",
            reference=secrets.token_hex(16).upper()
            
        )
        get_account.save(db)
        trxn.save(db)
    except Exception as e:
         return JSONResponse(status_code=403,
                        content={"message": str(e)}
                        )
    
    return {"message": "Deposit success",  "account": get_account ,"transaction": trxn,  }


@router.post("/transfer", status_code=status.HTTP_200_OK, operation_id="jwt_fresh_token_required")
def transfer(user_account: accounts.Transfer, db: Session = Depends(get_db),
             owner_id: str = Depends(current_user)):
    get_account = db.query(account.Account).filter_by(user_id=owner_id).first()
    destination = db.query(account.Account).filter_by(id=user_account.destination).first()
    if not destination:
        return JSONResponse(status_code=404,
                        content={"message": "destination user not found"}
                        )
    try:
        get_account.transfer(user_account.amount, destination)
        get_account.save(db)
        trxn = get_account.transactions.append(transaction.Transaction(
            amount=user_account.amount,
            user_id=owner_id,
            account_id=get_account.id,
            status="success",
            transaction_type="transfer",
            
        ))
        trxn.save(db)
    except Exception as e:
         return JSONResponse(status_code=403,
                        content={"message": str(e)}
                        )
    return {"message": "Transfer success", "account": get_account, "transaction": trxn}

   


@router.get("s", status_code=status.HTTP_200_OK, response_model=List[accounts.UserAccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    all_accounts = db.query(account.Account).all()
    return all_accounts
