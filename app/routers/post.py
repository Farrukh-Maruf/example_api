from typing import List, Optional
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schema
from .. database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    tags=["Posts"]
)


@router.get("/limit",response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10):

    print(f"bu limit{limit}")    
    posts = db.query(models.Post).all()
    # print(posts)
    return posts

@router.get("/create_posts", status_code=status.HTTP_201_CREATED, response_model = schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    # print(get_current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post

# @router.get("/posts", response_model = List[schema.Post])
@router.get("/posts", response_model=List[schema.PostOut] )
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #default limit 10, skip 0
    
    print(f"Bu postlarni limit {limit}")
    # hamma postlarni korsatadi,limit va offset tasiriga kora korsatadi, title lardan search orqali izlash mumkin
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    # posts = db.query(models.Post).filter(models.Post.owner_id== user_id.id).all()  # faqat o'z postlarini ko'rsatadi,  

    # perform a join to get vote counts along with posts, bu ikki table ni join qiladi
    results = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # {{URL}}posts?limit=2  bu postlarni 2ta qilib korsatadi

    print(results)
    return results

@router.post("/posts", status_code = status.HTTP_201_CREATED,response_model= schema.Post)
def create_posts(post : schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # agar login qilinmagan bolsa qayta post qila olmaydi, post qilish uchun login bolishi kerak, shuning user_id ni olamiz
    # no login, no post
    print(f"current user id is {current_user.id}")
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())   # agar create post qilsa faqat ozi uchun(current user)post qila oladi, va id ham ozini shaxsiy id si boladi
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post.title)
    return new_post

@router.get("/posts/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user) 

    post = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()      # birinchi post.id ni oladi, all() - hamma post.id ni oladi

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id{id} is not found')
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)   #deleting post and giving status code
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # print(post)
    # print(post.owner_id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post the id {id} is not found or doesnt exit")
    
    if post.owner_id != current_user.id:  #bu delete function faqat owner ozini postlarini ochirishga ruhsat beradi!!
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perfom, delete your own post!!")

    post_query.delete(synchronize_session = False) # this line actually deletes the row in database without synchro to speed up
    db.commit() 
    # return Response(status_code=status.HTTP_204_NO_CONTENT) # when u delete, 204 should send

@router.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} is not exist")
    
    if post.owner_id != current_user.id: # bu update function faqat owner ozini postlarini update qilishga ruhsat beradi!!
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not Authorized to update  other people posts, update ur own posts!!")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()