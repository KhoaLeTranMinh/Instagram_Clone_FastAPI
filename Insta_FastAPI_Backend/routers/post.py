
import shutil
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from auth.oauth2 import get_current_user
from db.models import DbPost
from .schemas import AuthenticatedUser, PostRequest, PostResponse
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_post
import string
import random
router = APIRouter(
    prefix='/post',
    tags=['post'] #for documentation
)

image_url_type = ['absolute','relative']

@router.post("",response_model= PostResponse) ##the problem is here!!!! response_model is PostDisplay, not PostBase, therefore there will be a conversion from DbPost to PostDisplay 
#also remember that PostDisplay is a class for Swagger documentation display 
#the name of the function will determine the name appeared on fastapi swagger
def create_post(request: PostRequest, db: Session = Depends(get_db), current_user: AuthenticatedUser = Depends(get_current_user))->DbPost:  #call on a function from a diff base for ourself
    if not request.image_url_type in image_url_type:
        raise HTTPException(status_code=400, detail="Invalid image_url_type, it must be either absolute or relative")
    return db_post.create_post(db,request)  
    
@router.get('/all', response_model= List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)
    
@router.post('/images')
def upload_image(image: UploadFile = File(...), current_user: AuthenticatedUser = Depends(get_current_user)):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(6))
    new = f'_{random_string}.'
    # print(image.filename.rsplit('.',1))  #split the filename into arrays, separated by a dot. khoa.jpeg would be come ['khoa','jpeg']
    filename = new.join(image.filename.rsplit('.',1)) #adding the random string in between the filename and the extension   
    path = f'images/{filename}'
    
    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file,buffer)
    return {'filename': path} 
    
@router.get('/delete/{id}')
def delete_post(id: int, db:Session= Depends(get_db) , current_user: AuthenticatedUser = Depends(get_current_user)):
    return db_post.delete(db, id, current_user.id)