from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from db import db_comment
from db.database import get_db
from routers.schemas import AuthenticatedUser, CommentRequest
router = APIRouter(
    prefix='/comment',
    tags=['comment'],
)

@router.get('/all/{post_id}')
def get_all_comments_from_post(post_id: int, db: Session  = Depends(get_db)):
    return db_comment.get_all_comments(db, post_id)
    
@router.post('')
def create_comment( request :CommentRequest,db: Session = Depends(get_db), current_user : AuthenticatedUser = Depends(get_current_user)):
    return db_comment.create_comment(db, request)
    
