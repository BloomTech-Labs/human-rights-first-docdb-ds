docker build . -t docdb
docker run -it -p 5000:5000 docdb uvicorn app.api:API --host=0.0.0.0 --port=5000
