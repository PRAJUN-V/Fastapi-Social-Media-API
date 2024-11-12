from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Default value is True if not provided
