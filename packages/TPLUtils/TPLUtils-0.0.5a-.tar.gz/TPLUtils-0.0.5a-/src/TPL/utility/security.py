from firebase_admin import auth
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from typing import Optional
from pydantic import BaseModel

from src.TPL.utility.logging import logger
from src.TPL.db.config import db


# !!! verify which one are not actually optional
class DecodedToken(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None
    iss: Optional[str] = None
    aud: Optional[str] = None
    auth_time: Optional[int] = None
    user_id: str
    sub: Optional[str] = None
    iat: Optional[int] = None
    exp: Optional[int] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    firebase: dict

    @staticmethod
    def get(decoded_token: dict):
        return DecodedToken(**decoded_token)


http_bearer = HTTPBearer()

def verify_user(bearer: str = Depends(http_bearer)) -> DecodedToken:
    try:
        decoded_token = auth.verify_id_token(bearer.credentials)
        return DecodedToken.get(decoded_token)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    
def verify_admin(bearer: str = Depends(http_bearer)) -> DecodedToken:
    try:
        decoded_token = auth.verify_id_token(bearer.credentials)
        users_ref = db.collection('users')
        user_ref = users_ref.document(decoded_token['uid'])
        if user_ref.get().to_dict()['role'] == 'admin':
            return DecodedToken.get(decoded_token)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin")