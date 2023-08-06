from pydantic import BaseModel
from typing import Optional
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from fastapi import HTTPException, status
import uuid
from enum import Enum

from src.TPL.utility.logging import logger
from src.TPL.db.config import db



class NewVariable(BaseModel):
    name: str
    value: str

class WebsiteType(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"


class NewWebsite(BaseModel):
    description: str
    repo_name: str
    port_number: Optional[str] = None
    type: WebsiteType



class Website(BaseModel):
    website_id: Optional[str]
    created_at: DatetimeWithNanoseconds
    description: str
    env: dict
    name: str
    owner_id: str
    port_number: str
    repo_name: str
    type: WebsiteType
    updated_at: Optional[DatetimeWithNanoseconds]

    def save(self):
        data = self.dict(exclude={'website_id'})
        website_ref = db.collection('websites').document(self.website_id)
        website_ref.set(data)

    def to_dict(self):
        return self.dict(exclude={'env'})
    
    def delete(self):
        website_ref = db.collection('websites').document(self.website_id)
        website_ref.delete()

    @staticmethod
    def create(website_data: dict) -> 'Website':
        new_website_id = str(uuid.uuid4())
        website_data["website_id"] = new_website_id
        new_website = Website(**website_data)
        new_website.save()
        return new_website
    
    @staticmethod
    def get_from_id(website_id: str):
        website_ref = db.collection('websites').document(website_id)
        try:
            website = website_ref.get().to_dict()
            website["website_id"] = website_id
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Website not found")
        return Website(**website)
    
    @staticmethod
    def get_from_user(website_name: str, user_id: str):
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get().to_dict()
        try :
            website_id = user['websites'][website_name]
            website: Website = Website.get_from_id(website_id)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Website not found")
        return website
