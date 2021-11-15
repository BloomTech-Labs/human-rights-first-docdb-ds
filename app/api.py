"""
Labs DS Machine Learning Operations Role
- Application Programming Interface
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.box_wrapper import BoxWrapper
from app.data import Data

API = FastAPI(
    title='Lambda School Labs Data Science API',
    version="0.0.4",
    docs_url='/',
)
API.db = Data()
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.post("/search/{query}")
async def search(query: str, projection: dict = None):
    return {"Result": list(API.db.search(query, projection))}


@API.post("/docview/{file_id}")
async def docview(file_id: str, projection: dict = None):
    return API.db.find_one({"id": file_id}, projection)


@API.put("/add_tag/{file_id}{new_tag}")
async def add_tag(file_id: str, new_tag: str):
    API.db.add_tag(file_id, new_tag)
    return {'Result': 'Success'}

if __name__ == '__main__':
    uvicorn.run(API)
