from fastapi import FastAPI, Response, status, HTTPException
from app.schemas import Post
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# PostgreSQL connection setup
while True:
    try:
        # Connect to your PostgreSQL DB
        conn = psycopg2.connect(
            dbname="fastapi",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor  # Use RealDictCursor to get dictionary-like rows
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as e:
        print("Connecting to database failed")
        print(f"Error: {e}")
        time.sleep(3)

# 1. Get All Posts
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return {"data": posts}

# 2. Create a New Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """
        INSERT INTO post (title, content, published) 
        VALUES (%s, %s, %s) 
        RETURNING id, title, content, published, created_at;
        """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()  # Commit the transaction
    return {"data": new_post}

# 3. Get an Individual Post
@app.get("/posts/{id}")
def get_individual_post(id: int):
    cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": post}

# 4. Delete a Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING id;", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()  # Commit the transaction

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# 5. Update a Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE post 
        SET title = %s, content = %s, published = %s, created_at = NOW()
        WHERE id = %s
        RETURNING id, title, content, published, created_at;
        """,
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()  # Commit the transaction

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    return {"data": updated_post}
