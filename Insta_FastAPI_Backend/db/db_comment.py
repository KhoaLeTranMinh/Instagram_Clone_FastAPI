from datetime import datetime
from sqlalchemy.orm.session import Session
from db.models import DbComment
from routers.schemas import CommentRequest
from fastapi import HTTPException, status
def create_comment(db: Session, request: CommentRequest):
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        timestamp = datetime.now(),
        post_id = request.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
    
def get_all_comments(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()
    
    
