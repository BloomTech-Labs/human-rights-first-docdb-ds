import os
import re

import pytesseract
from boto3 import Session
from dotenv import load_dotenv
from pdf2image import convert_from_bytes


load_dotenv()

uuid = "007a58f2-894d-424f-824a-2b281ea5b00f"

s3 = Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
).client("s3")
response = s3.get_object(
    Bucket=os.getenv("BUCKET_NAME"),
    Key=f"{uuid}.pdf",
)

pages = convert_from_bytes(response["Body"].read(), dpi=90)
text = " ".join(map(pytesseract.image_to_string, pages))
clean_text = re.sub(r"\s+", " ", text)

print(clean_text[:1000])
