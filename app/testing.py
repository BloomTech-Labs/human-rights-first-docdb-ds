import os
import re
from pdf2image import convert_from_path, convert_from_bytes
import pytesseract
from dotenv import load_dotenv
from boxsdk import Client, OAuth2

load_dotenv()

# Create client and authorization
auth = OAuth2(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    access_token=os.getenv('DEVELOPER_TOKEN')
)

client = Client(auth)

# # Download file from Box
file_id = 844529989327
file_content = client.file(file_id).content()

# Set user
me = client.user().get()

# Get user's root folder
root_folder = client.root_folder().get()

# Get information on the items in user's root folder
fields = [
    'type',
    'id',
    'name'
]

items = client.folder(root_folder.id).get_items(fields=fields)
for item in items:
    print(item.type, item.id, item.name)

# Code to run OCR on downloaded Box files
pages = convert_from_bytes(file_content, dpi=90)
text = " ".join(map(pytesseract.image_to_string, pages))
clean_text = re.sub(r"\s+", " ", text)
print(clean_text)