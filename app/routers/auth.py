from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

from .. import database, schema, models, utils, oauth2


router = APIRouter(
    tags=["Authentication"]   
)

@router.post('/login', response_model = schema.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): # OAuth2PasswordRequestForm gives username and password fields, 

    #token bu login ni authorize qilish uchun kerak, 
    #username
    #password qaytadi
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"invalid(user) credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"invalid credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
