from firebase_admin import credentials, initialize_app, firestore
import os

from src.TPL.utility.logging import logger


# initialize firebase auth and db
try :
    key_file_path = os.environ.get("TPL_FIREBASE_AUTH")
    cred = credentials.Certificate(key_file_path)
    initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase initialized")
except Exception as e:
    logger.info("Firebase initialization failed: remember to set the environment variable TPL_FIREBASE_AUTH")
    logger.error(e)
    db = None