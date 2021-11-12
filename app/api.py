from boxsdk import BoxAPIException
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.box_wrapper import BoxWrapper
from app.data import Data

API = FastAPI(
    title='DocDB Data Science API',
    version="0.40.6",
    docs_url='/',
)
API.db = Data()
API.box = BoxWrapper()
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/search/{query}")
async def search(query: str):
    return {"Response": list(API.db.search(query))}


@API.get("/lookup/{file_id}")
async def lookup(file_id: str):
    return {"Response": API.db.find_one({"box_id": file_id})}


@API.get("/thumbnail/{file_id}")
async def thumbnail(file_id: str):
    try:
        return Response(API.box.get_thumbnail(file_id), media_type="image/jpg")
    except BoxAPIException:
        return FileResponse("app/images/not-found-icon.jpg", media_type="image/jpg")


if __name__ == '__main__':
    uvicorn.run(API)
