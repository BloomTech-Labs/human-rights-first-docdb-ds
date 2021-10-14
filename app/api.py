"""
Labs DS Machine Learning Operations Role
- Application Programming Interface
"""
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


API = FastAPI(
    title='Lambda School Labs Data Science API',
    version="0.0.2",
    docs_url='/',
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(API)
