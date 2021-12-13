import os
from os.path import exists

from boto3.session import Session

from app.box_wrapper import BoxWrapper


box = BoxWrapper()

s3 = Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
).client('s3')

with open("inserted.csv", "r") as f:
    box_ids = (
        line.split(",")[-1].strip() for line in f.readlines()
        if line.startswith("file")
    )
skip_list = {
    "455229161973.jpg",
    "455196133662.jpg",
    "455197285912.jpg",
    "455192922518.jpg",
    "455206068325.jpg",
    "455197575319.jpg",
    "455230304948.jpg",
    "455231112224.jpg",
}
for idx, box_id in enumerate(box_ids, 1):
    file_name = f"{box_id}.jpg"
    file_path = f"thumbnails/{file_name}"
    if not exists(file_path) and file_name not in skip_list:
        print(f"\nFile: {idx}")
        print(f"  Downloading '{file_name}' from Box")
        size = 160
        file_bytes = box.get_thumbnail(box_id)
        with open(file_path, 'wb') as file:
            print(f"  Saving '{file_name}' locally")
            file.write(file_bytes)
        with open(file_path, "rb") as file:
            print(f"  Uploading '{file_name}' to AWS S3")
            s3.upload_fileobj(file, os.getenv("S3_BUCKET"), file_name)
    else:
        print(f"Skipping {file_name}")
