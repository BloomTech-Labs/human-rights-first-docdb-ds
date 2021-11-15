from boxsdk import BoxOAuthException
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.box_wrapper import BoxWrapper
from app.data import Data

API = FastAPI(
    title='DocDB Data Science API',
    version="0.40.7",
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
    """ Returns everything but the text for all search matches
    Example: http://human-rights-first-docdb-ds-dev.us-east-1.elasticbeanstalk.com/search/London%20England

    {'Response': [{'box_id': String,
    'name': String,
    'path': String,
    'url': String,
    'tags': Array of Strings}]}
    """
    return {"Response": list(API.db.search(query))}


@API.get("/lookup/{file_id}")
async def lookup(file_id: str):
    """ Returns everything for a single match
    Example: http://human-rights-first-docdb-ds-dev.us-east-1.elasticbeanstalk.com/lookup/76737668329

    {'Response': {'box_id': String,
    'name': String,
    'path': String,
    'url': String,
    'tags': Array of Strings,
    'text': String}}
    """
    return {"Response": API.db.find_one({"box_id": file_id})}


@API.get("/thumbnail/{file_id}")
async def thumbnail(file_id: str):
    """ Returns the jpg thumbnail for a single document,
    Returns a default image if document is not found.
    """
    try:
        return Response(API.box.get_thumbnail(file_id), media_type="image/jpg")
    except BoxOAuthException:
        return FileResponse("app/images/default.jpg", media_type="image/jpg")


if __name__ == '__main__':
    uvicorn.run(API)
