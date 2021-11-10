"""
Labs DS Machine Learning Operations Role
- Application Programming Interface
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
async def search(query: str):
    return {"Result": list(API.db.search(query))}


@API.post("/docview/{file_id}")
async def docview(file_id: str):
    return API.db.find({"id": file_id}, {"_id": False})[0]

if __name__ == '__main__':
    uvicorn.run(API)
