from app.nlp import get_entities
from app.box_wrapper import BoxWrapper
from app.ocr import ocr
from app.data import Data

box = BoxWrapper()


def update_csv(completed_type, completed_id):
    with open('inserted.csv', 'a') as f:
        f.write(f"{completed_type},{completed_id}\n")


def get_finished():
    finished_dict = {}
    with open('inserted.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if ',' not in line:
                continue
            item_type, item_id = line.rstrip().split(",")
            if item_type == "file" or item_type == "folder_complete":
                finished_dict[item_id] = 1
            else:
                finished_dict[item_id] = 0
    return finished_dict


def iterate_main_folder():
    files, folders = box.items_in_folder()
    finished = get_finished()
    for fold in folders:
        iterate_folder_items(fold.id, finished)


def iterate_folder_items(folder_id, finished):
    if folder_id in finished.keys():
        if finished[folder_id] == 1:
            print("Closed folder: " + folder_id)
            return

    files, folders = box.items_in_folder(folder_id)
    update_csv("folder_in_progress", folder_id)
    print("Working on folder: " + folder_id)
    for fold in folders:
        iterate_folder_items(fold['id'], finished)
    for fil in files:
        insert_record(fil['id'], finished)
    update_csv("folder_complete", folder_id)
    print("Completed folder: " + folder_id)


def insert_record(file_id, finished):
    if file_id in finished.keys():
        print("Closed File: " + file_id)
        return
    info = box.get_file_info(file_id)
    if info["ext"] != "pdf":
        return

    print("inserting file: " + file_id)
    record = {
        'id': info['id'],
        'name': info['name'],
        'path': info['path'],
        'url': info['url'],
        'raw_text': ocr(box.download_file(file_id), dpi=150)
    }

    record['tags'] = get_entities(record['raw_text'])

    db = Data()

    db.insert([record])
    update_csv("file", file_id)
    return


if __name__ == '__main__':
    fin = get_finished()
    iterate_folder_items('2761659211', finished=fin)
