import os
from math import ceil

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.aws_s3 import S3
from app.mongo import MongoDB

API = FastAPI(
    title='DocDB DS API',
    version="0.42.1",
    docs_url='/',
)
API.db = MongoDB()
API.s3 = S3()

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version")
async def version():
    return API.version


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
    'summary': String,
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
    file_name = f"{file_id}.jpg"
    file_path = f"app/thumbnails/{file_name}"
    if not os.path.exists(file_path):
        API.s3.download("docdb-thumbnails", file_name, file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpg")
    else:
        return FileResponse("app/thumbnails/default.jpg", media_type="image/jpg")


@API.get("/raw_text/{file_id}")
async def raw_text(file_id: str):
    file = API.db.find_one({"box_id": file_id})
    file_name = file["name"].replace(".pdf", ".txt")
    file_path = f"app/text-files/{file_name}"
    with open(file_path, "w") as f:
        f.write(file["text"])
    return FileResponse(file_path, media_type="text/plain")


@API.post("/add_tag")
async def add_tag(file_id: str = Form(...), tag: str = Form(...)):
    """ Adds a custom tag to a document """
    API.db.push_list({"box_id": file_id}, "tags", tag)
    return {'Result': 'Success', "file_id": file_id, "tag": tag}


@API.delete("/remove_tag")
async def remove_tag(file_id: str, tag: str):
    """ Removes a tag from a document """
    API.db.pull_list({"box_id": file_id}, "tags", tag)
    return {'Result': 'Success', "file_id": file_id, "tag": tag}
