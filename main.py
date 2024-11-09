from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

my_posts = []

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if user doesn't provide it should be defaulted True
    rating: Optional['int'] = None # if rating is not given it return None value.

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
@app.get("/")
def root(): # this is path operation function we can name it anything, but ideally it is better to use a descriptive name.
    return {"message": "Hello world"}

@app.post("/post-without-data-validation")
def create_post_without_data_validation(payload: dict = Body(...)): # Data sending without data validation, here Body from request is converted to dict and store in a variable named payload
    print(payload)
    return payload

@app.post("/create-post")
def create_post(new_post: Post): # Data sending with data validation
    print(new_post)
    return {"data": "new post"}

# We are going to create CRUD operations in post in social media by best practice.

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict() # converting a pydantic object to dict
    post_dict["id"] = randrange(0, 1000000)
    print(post_dict)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # we can use this directly in place of 2 codes which is commented below.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id :{id} not found."}
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

