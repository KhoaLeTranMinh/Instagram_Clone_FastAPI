from fastapi import APIRouter,Depends
from .schemas import  UserRequest, UserResponse
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user

router = APIRouter(
    prefix='/user',
    tags=['user'] #for documentation
)

@router.post("",response_model= UserResponse)
def create_user(request: UserRequest, db: Session = Depends(get_db))->UserResponse: #call on a function from a diff base for ourself
    return db_user.create_user(db,request)