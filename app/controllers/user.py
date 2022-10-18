from typing import List, Union

from fastapi import APIRouter, Depends

from app.utils.pagination import pagination
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import users
from ..schemas.users import SingleUser, UpdateUser, PaginationUserSchema
from ..utils import jwt

router = APIRouter()


@router.get("", response_model=SingleUser, operation_id="jwt_required")
def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(jwt.current_user)):
    user = db.query(users.User).filter_by(id=user_id).first()
    return user


@router.put("/{user_id}", response_model=SingleUser)
def update_user(payload: UpdateUser, user_id: str, db: Session = Depends(get_db)):
    user = db.query(users.User).filter_by(id=user_id).first()
    
    user.update(payload)
    user.save(db)
    return user

@router.get("s", response_model=PaginationUserSchema)
def get_users(db: Session = Depends(get_db), name: Union[str, None]= None, 
                    email : Union[str, None]= None,  limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    end = skip + limit
    params = {"name": name,"email": email, "limit": limit, "offset": skip}
    all_users = users.User.search(params, db)
    response = {"users": all_users, "pagination": {"limit": limit, "page": page,  "total": len(all_users)}}
    pagination(end, page, response, len(all_users))

    # all_users= db.query(users.User).filter_by(**params).all()
    return response
