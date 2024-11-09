from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if user doesn't provide it should be defaulted True
    rating: Optional['int'] = None # if rating is not given it return None value.

@app.get("/")
def root(): # this is path operation function we can name it anything, but ideally it is better to use a descriptive name.
    return {"message": "Hello world"}

@app.get("/posts")
def get_post():
    return {"data": "This is your post."}

@app.post("/post-without-data-validation")
def create_post_without_data_validation(payload: dict = Body(...)): # Data sending without data validation, here Body from request is converted to dict and store in a variable named payload
    print(payload)
    return payload

@app.post("/create-post")
def create_post(new_post: Post): # Data sending with data validation
    print(new_post)
    return {"data": "new post"}


