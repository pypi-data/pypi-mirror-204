
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Optional

from src.TPL.db.config import db
from src.TPL.utility.logging import logger

class User(BaseModel):
    '''
    User class
    '''
    user_id: str
    username: str

    allowed_deployments: int
    created_at: DatetimeWithNanoseconds
    updated_at: Optional[DatetimeWithNanoseconds]
    
    fname: str
    lname: str

    email: str
    github: str
    linkedin: str
    phone: str

    photo_url: str
    
    role: str
    
    # example:
    # {
    #    "<website_name>": "<website_id>",
    #    "<website_name1>": "<website_id1>", 
    #    ...
    # }
    websites: dict

    @staticmethod
    def create(user_data: dict) -> 'User':
        user_data["created_at"] = DatetimeWithNanoseconds.now()
        new_user = User(**user_data)
        new_user.save()
        return new_user

    def save(self) -> None:
        '''
        Save user to database
        '''
        data = self.dict(exclude={'user_id'})
        user_ref = db.collection('users').document(self.user_id)
        user_ref.set(data)

    @staticmethod
    def get(user_id: str) -> 'User':
        '''
        Get user by user_id
        '''
        user_ref = db.collection('users').document(user_id)
        try:
            user = user_ref.get().to_dict()
            user["user_id"] = user_id
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User(**user)
    
    @staticmethod
    def get_from_username(username: str) -> 'User':
        '''
        Get user by username
        '''
        users_ref = db.collection('users')
        users = users_ref.where('username', '==', username).stream()
        for user in users:
            return User.get(user.id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
