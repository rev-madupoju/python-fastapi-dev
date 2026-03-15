from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello from fcc-api-dev"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app")