from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models  
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#secret key
#algorithm
#expiration time

SECRET_KEY = settings.secret_key # should be kept secret, handles encoding and decoding of JWT tokens
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # login time in minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):   #user token ni oladi va tekshiradi, agarda to'g'ri bo'lsa token data ni qaytaradi
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #bu yerda tokenni ochadi, va ichidan user_id ni oladi
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data # token data bu id ni o'z ichiga oladi

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):   #user toke ni oladi, va tekshiradi,  agarda to'g'ri bo'lsa user ni qaytaradi
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = f"Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user