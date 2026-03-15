from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime


class Post(BaseModel):
    title: str = Field(default_factory=lambda: datetime.now().strftime("Untitled_%Y%m%d_%H%M%S"))
    desc: str | None = Field(default=None, max_length=100)
    post_type: Literal["image", "audio", "reel", "hybrid"] = "image"
    
class PostCreate(Post):
    tags: list[str] | None = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="milliseconds"))
    created_by: str 

class PostResponse(PostCreate):
    status: Literal["published", "published-modified", "archived", "deleted"] = "published"
    updated_at: str | None = None

class PostModified(PostResponse):
    status = "published-modified"
    updated_at: str | None = Field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="milliseconds"))

    @field_validator("status")
    @classmethod
    def prevent_published_status(cls, v):
        if v == "published":
            raise ValueError("A modified post cannot have 'published' status.")
        return v


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello from fcc-api-dev"}


my_posts: list[PostResponse] = [
    PostResponse(desc="first post", created_by="myself"),
    PostResponse(title="21st Birthday Post", created_by="Bob"),
]


@app.post("/posts")
def create_post(post: Post) -> PostCreate:
    post_data = post.model_dump() 

    full_post_data = {
        **post_data, 
        "tags": {"new", "trending"}, 
        "timestamp": datetime.now().isoformat(sep=" ", timespec="milliseconds")
    }
  
    return PostCreate(**full_post_data)


@app.get("/posts")
def get_posts() -> list[PostResponse]:
    if len(my_posts) == 0:
        return list()
    dummy_posts = [p for p in my_posts]
    return dummy_posts


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app")