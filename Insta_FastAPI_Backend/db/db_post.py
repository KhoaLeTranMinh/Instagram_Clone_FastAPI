import datetime
from fastapi import HTTPException,status
from .models import DbPost
from routers.schemas import  PostRequest
from sqlalchemy.orm.session import Session

def create_post(db: Session, request: PostRequest):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.datetime.now(),
        user_id = request.creator_id
    )
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
def get_all(db: Session):
    return db.query(DbPost).all()
    
def delete(db: Session, id: int, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Post with id {id} was not found')
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorized to delete this post')
    db.delete(post)
    db.commit()
    return 'ok'

