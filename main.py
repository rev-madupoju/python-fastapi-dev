from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class Post(BaseModel):
    title: str
    desc: str | None
    post_type: Literal["image", "reel", "hybrid"]
    
class PostCreate(Post):
    tags: set[str] | None
    timestamp: str

class PostResponse(Post):
    status: Literal["published"] | Literal["archived"] = "published"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello from fcc-api-dev"}


@app.get("/posts")
def get_posts():
    return {"data": {"post1": "p1", "post2": "p2"}}


@app.post("/posts")
def create_post(new_post: Post) -> PostCreate:
    post_data = new_post.model_dump() 

    full_post_data = {
        **post_data, 
        "tags": {"new", "trending"}, 
        "timestamp": datetime.now().isoformat(sep=" ", timespec="milliseconds")
    }
  
    return PostCreate(**full_post_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app")