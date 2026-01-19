from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login") #it could be anything but must match the login path in auth.py
from .config import settings

#SECRET KEY
#ALgorithm  HS256
#Expiration Time

# SECRET_KEY ="mysecretkey1234justforlearningpurpose"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def create_access_token(data: dict):
    to_encode = data.copy()
    #expiration field
    #expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) when hardcoded
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token : str = Depends(oauth2_scheme),db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = "Could not validate credentials",
                                          headers = {"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user




