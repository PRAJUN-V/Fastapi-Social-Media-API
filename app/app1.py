from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from app.models import engine, SQLAlchemyPost
from sqlalchemy.orm import sessionmaker

app = FastAPI()

Session = sessionmaker(bind=engine)
session = Session()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Default value is True if not provided

@app.get("/posts")
def get_posts():
    posts = session.query(SQLAlchemyPost).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = SQLAlchemyPost(title=post.title, content=post.content, published=post.published)
    session.add(post)
    session.commit()
    return {"message": "new post is added"}

@app.get("/posts/{id}")
def get_individual_post(id: int):
    post = session.query(SQLAlchemyPost).filter_by(id=id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = session.query(SQLAlchemyPost).filter_by(id=id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    session.delete(deleted_post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post = session.query(SQLAlchemyPost).filter_by(id=id).first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    updated_post.title = post.title
    updated_post.content = post.content
    session.commit()
    return {"message": "Post updated"}
