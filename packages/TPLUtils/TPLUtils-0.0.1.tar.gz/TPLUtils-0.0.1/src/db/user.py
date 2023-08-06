from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel
from fastapi import HTTPException, status

from db.config import db
from utility.logging import logger

class User(BaseModel):
    user_id: str
    allowed_deployments: int
    created_at: DatetimeWithNanoseconds
    email: str
    fname: str
    github: str
    linkedin: str
    lname: str
    phone: str
    photo_url: str
    role: str
    username: str
    websites: dict

    def save(self) -> None:
        data = self.dict(exclude={'user_id'})
        user_ref = db.collection('users').document(self.user_id)
        user_ref.set(data)

    @staticmethod
    def get(user_id: str) -> 'User':
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
        users_ref = db.collection('users')
        users = users_ref.where('username', '==', username).stream()
        for user in users:
            return User.get(user.id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
