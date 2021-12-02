from boxsdk import BoxOAuthException, BoxAPIException
from fastapi import FastAPI, Form
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.box_wrapper import BoxWrapper
from app.data import Data

API = FastAPI(
    title='DocDB DS API',
    version="0.41.1",
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

    Example: https://ds.humanrightsfirstdocdb.dev/search/London%20England

    Response Object with a Array of JSON Objects:

    {'Response': [{'box_id': String,
    'name': String,
    'path': String,
    'url': String,
    'tags': Array of Strings}]}
    """
    return {"Response": list(API.db.search(query)[:32])}


@API.get("/lookup/{file_id}")
async def lookup(file_id: str):
    """ Returns everything for a single match

    Example: https://ds.humanrightsfirstdocdb.dev/lookup/76737668329

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
    """ WORK IN PROGRESS!!!

    Returns the jpg thumbnail for a single document.

    Returns a default image on Box error.
    This is common while we have a "developer" Box account.
    """
    try:
        return Response(API.box.get_thumbnail(file_id), media_type="image/jpg")
    except BoxAPIException:
        return FileResponse("app/images/default-160x160.jpg", media_type="image/jpg")
    except BoxOAuthException:
        return FileResponse("app/images/default-160x160.jpg", media_type="image/jpg")


@API.post("/add_tag")
async def add_tag(file_id: str = Form(...), tag: str = Form(...)):
    """ Adds a custom tag to a document """
    API.db.add_tag(file_id, tag)
    return {'Result': 'Success', "file_id": file_id, "tag": tag}


@API.delete("/remove_tag")
async def remove_tag(file_id: str = Form(...), tag: str = Form(...)):
    """ Removes a tag from a document """
    API.db.remove_tag(file_id, tag)
    return {'Result': 'Success', "file_id": file_id, "tag": tag}


@API.get("/backup")
async def backup():
    return API.db.backup()

if __name__ == '__main__':
    uvicorn.run(API)
