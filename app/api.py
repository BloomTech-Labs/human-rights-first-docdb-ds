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
    if 'thumbnail' in projection.keys():
        thumbnail = projection.pop('thumbnail')
    else:
        thumbnail = False
    results = list(API.db.search(query, projection))
    if thumbnail:
        box = BoxWrapper()
        for result in results:
            result['thumbnail'] = str(box.get_thumbnail(result['id']))
    return {"Result": results}


@API.post("/docview/{file_id}")
async def docview(file_id: str, projection: dict = None):
    return API.db.find_one({"id": file_id}, projection)

if __name__ == '__main__':
    uvicorn.run(API)
