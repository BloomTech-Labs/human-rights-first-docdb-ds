import os
from math import ceil

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.box_wrapper import BoxWrapper
from app.data import Data

API = FastAPI(
    title='DocDB DS API',
    version="0.41.4",
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


@API.get("/search")
async def get_search(query: str):
    return {"Response": list(API.db.search(query)[:32])}


@API.post("/search")
async def search(query: str, page_number: int = 0, results_per_page: int = 100):
    start = page_number * results_per_page
    stop = start + results_per_page
    search_results = API.db.search(query)[start:stop]
    count = API.db.count({"$text": {"$search": query}})
    n_pages = ceil(count / results_per_page)
    return {"Pages": n_pages, "Count": count, "Response": list(search_results)}


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
    """ Returns the jpg thumbnail for a single document.
    Returns default image on error.
    """
    file_path = f"app/thumbnails/{file_id}.jpg"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpg")
    else:
        return FileResponse("app/thumbnails/default.jpg", media_type="image/jpg")


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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(API)
