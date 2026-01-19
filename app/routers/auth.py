from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm




router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token) # call this anything S called it login
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #login logic
    # {
    #     "username": "someusrname", anything that user sends here its email
    #     "password": "password-somepassword"
    # }
    # OAuth2PasswordRequestForm has username and password fields by default and no email field



    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                detail = f"Invalid Credentials")
    if not utils.compare_pass(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                detail = f"Invalid Credentials")
    #create a token and return
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    # data is what I wanna provide i can do more fields if wanted or needed whatever
    return {"access_token": access_token, "token_type": "bearer"}


