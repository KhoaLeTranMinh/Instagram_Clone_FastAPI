from datetime import datetime
import string
from typing import List
from pydantic import BaseModel


class UserRequest(BaseModel): #UserRequest
    username: str
    email: str
    password: str

class UserResponse(BaseModel): #UserResponse
    username: str
    email: str
    class Config(): # part of pydantic feature
        from_attributes = True #orm_mode name changed to from attributes
        
class PostRequest(BaseModel):
    image_url: str
    image_url_type: str #absolute or relative
    caption: str
    creator_id: int
    
 #For Post Display
class UserForPostResponse(BaseModel):
    username: str    #was user_name, now changed to username
    class Config():
        from_attributes = True

class CommentForPostDisplay(BaseModel):
    text: str
    username: str
    timestamp: datetime
    class Config():
        from_attributes = True
        
class PostResponse(BaseModel):
    id:int
    image_url: str
    image_url_type: str
    timestamp: datetime
    user:UserForPostResponse
    comments: List[CommentForPostDisplay]
    class Config():
        from_attributes = True
        
class AuthenticatedUser(BaseModel):
    id: int
    username: str
    email: str
    
class CommentRequest(BaseModel):
    username: str
    text: str
    post_id: int