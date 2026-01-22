from .. import models, schemas, oauth2
from typing import List, Optional
from fastapi import Body, FastAPI, status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
    )

#@app.get("/posts", response_model=schemas.Post) bcz we need a list of post not one individual so we need List from typing
@router.get("/",response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
              limit:int = 10, skip:int = 0,search : Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(posts)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
        ).limit(limit).offset(skip).all() # to get all posts like in Social Media apps .all() gets all records
    #print(current_user.id) just for debugging
    #posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() #returns posts of logged in user only - like in notes app
    #print(posts) - returns raw sql query
    # print(limit)
    # print(search) - #%20 is space in url encoding
    # print(skip)
    results = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("n_votes")
        ).join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()

    #reason for isouter=True is to get posts even if they have 0 votes and sqlalchemy by default does inner join
    #whereas SQL joins are outr by default
    
    return results



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.publish))
    # conn.commit()
    # newPost = cursor.fetchone()
    #print(post.model_dump()) - pydantic model creates a dict of the post

    #if there's more column in table writing all manually is inefficient so we do
    #newPost = models.Post(**post.model_dump()) ** unpacks the dict and send the required column as parameter automatically

    # newPost = models.Post(title=post.title,content=post.content,published=post.publish)
    # above is the messay and manual way to do the same below is cleaner better way
    
    newPost = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(newPost) #to add
    db.commit() # to commit like above sql query
    db.refresh(newPost) #to get created post returned in sqlalchemy
    return newPost



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    # print(post)

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("n_votes")
        ).join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()
    #logging.info(post.__dict__) #not needed just to see post printed in terminal safer+reliable than print()
    #.__dict__ unpacks the value, colmns in this case
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} wasn't found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized")
    # the above is to make sure only owner can see one of his posts with specific id
    
    return post



@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # print(deleted_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.publish, id))
    # updatedPost = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) #to find post with specific id
    post = post_query.first() #grab that specific post

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} doesn't exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False) #post_query does exist so now update it
    db.commit() #commit to db
    return post_query.first()