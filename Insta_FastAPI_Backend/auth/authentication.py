from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from auth.oauth2 import create_access_token
from db.database import get_db
from db.models import DbUser
from db.hashing import Hash
router = APIRouter(
    # prefix="/authentication",
    tags=["authentication"],
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username ==  request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials', message='Invalid credentials')
    if not Hash.verify(user.password, request.password):
        print('lmao')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
        
    access_token = create_access_token(data={'username': user.username})
    
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }