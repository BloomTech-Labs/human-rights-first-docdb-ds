from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


API = FastAPI(
    title='Lambda School Labs Data Science API',
    version="0.0.1",
    docs_url='/',
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/home/")
async def home():
    return {
        "status": 200,
        "message": "Hello, world!"
    }


if __name__ == '__main__':
    uvicorn.run(API)
