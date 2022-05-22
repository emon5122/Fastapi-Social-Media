from typing import AsyncIterable
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Does it work?"}

@app.get("/app")
def jhsad():
    return{'title': 'it works'}

@app.get('/test')
def test():
    return {"message": "try"}