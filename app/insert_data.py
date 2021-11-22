""" Grabs files from Box, runs OCR on each and stores the data to MongoDB """
from os.path import exists

from app.nlp import get_tags
from app.box_wrapper import BoxWrapper
from app.ocr import ocr
from app.data import Data

box = BoxWrapper()
db = Data()
skip_list = (
    "25872996609", "25874329495", "25921860097",
    "455230304948", "455231112224",
)


def update_csv(completed_type, completed_id):
    with open('inserted.csv', 'a') as f:
        f.write(f"{completed_type},{completed_id}\n")


def get_finished():
    finished_dict = {}
    if not exists('inserted.csv'):
        with open('inserted.csv', 'w'):
            return finished_dict
    with open('inserted.csv', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if ',' in line:
            item_type, item_id = line.rstrip().split(",")
            if item_type == "file" or item_type == "folder_complete":
                finished_dict[item_id] = 1
            else:
                finished_dict[item_id] = 0
    return finished_dict


def iterate_folder_items(folder_id, finished):
    if finished.get(folder_id) == 1:
        print(f"Closed folder: {folder_id}")
        return

    files, folders = box.items_in_folder(folder_id)
    update_csv("folder_in_progress", folder_id)
    print(f"Working on folder: {folder_id}")
    for folder in folders:
        iterate_folder_items(folder['id'], finished)
    for file in files:
        insert_record(file['id'], finished)
    update_csv("folder_complete", folder_id)
    print(f"Completed folder: {folder_id}")


def insert_record(file_id, finished):
    if file_id in skip_list:
        print(f"Skipping file: {file_id}")
        return
    if file_id in finished.keys():
        print("Closed file: " + file_id)
        return
    info = box.get_file_info(file_id)
    if info["ext"] != "pdf":
        return

    print(f"Downloading file: {file_id}")
    file = box.download_file(file_id)
    print(f"OCR file: {file_id}")
    ocr_text = ocr(file, dpi=300)
    record = {
        'box_id': info['id'],
        'name': info['name'],
        'path': info['path'],
        'url': info['url'],
        'text': ocr_text,
        'tags': get_tags(ocr_text),
    }
    print(f"Inserting file: {file_id}")
    db.insert(record)
    update_csv("file", file_id)


if __name__ == '__main__':
    iterate_folder_items('855631806', finished=get_finished())
