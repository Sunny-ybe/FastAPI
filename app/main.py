from fastapi import FastAPI
from random import randrange
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings



import logging #in servers print() fails for multiple reasons so we use logging to see what's happening
logging.basicConfig(level=logging.INFO)

#to create the engine and all of our models 
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

# my_posts = [{"title":"title of post 1", "content":"content of post 1", "id": 1},
#             {"title": "hated food","content": "I hate pizza", "id":2}
#             ] initial dummy manual data in array of dict


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p 


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
def root():
    return {"message": "Hello Sunny"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": posts}
# test route 







#main file is getting too big we can split into multiple files one where all the path operations exist
# and other where the we deal with users - this is called Routers in FastAPI