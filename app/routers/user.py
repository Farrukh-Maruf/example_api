from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from .. import models, schema, utils
from .. database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Users"]
)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model = schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password, means that we protect the password in database,
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


@router.get("/users", response_model = List[schema.UserCreate])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    print(users)
    return users



@router.get("/user/{id}", response_model = schema.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id {id} is not found")
    return user



@router.put("/users/{id}", response_model=schema.UserCreate)
def update_user(id: int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id) 
    users = user_query.first() 

    if users == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} is not exist")

    user_query.update(updated_user.dict(), synchronize_session=False) 

    db.commit()
    return user_query.first()