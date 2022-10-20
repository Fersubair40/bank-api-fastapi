
from typing import Union
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import transaction, users

from app.schemas.transaction import TransactionResponse
from sqlalchemy.orm import Session

from app.utils.jwt import current_user
from app.utils.pagination import pagination
from sqlalchemy.sql import func
from fastapi.responses import JSONResponse



router = APIRouter()


@router.get("",)
def get_users_transactions(db: Session = Depends(get_db), user_id: str = Depends(current_user),
       amount: Union[int, None]= None, transaction_type: Union[str, None]= None,  
       status: Union[str, None]= None, 
       limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    end = skip + limit
    params = {"amount": amount,"transaction_type": transaction_type, "status": status, "limit": limit, "offset": skip}
    user = db.query(users.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

        
    transaction_count = db.query(func.count()).select_from(transaction.Transaction).filter_by(user_id=user.id).scalar()
    try:
        
        users_transactions = transaction.Transaction.search(params, db, user.id)
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={"message": str(e)})
    response = {"transactions": users_transactions, "pagination": {"limit": limit, "page": page,  "total": transaction_count}}
    pagination(end, page, response, transaction_count)
    return response
        
    
