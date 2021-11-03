from typing import Union, Tuple

from dotenv import load_dotenv
from os import getenv
from boxsdk import OAuth2, Client


class BoxWrapper:
    load_dotenv()
    token = getenv("DEVELOPER_TOKEN", default="0")
    id = getenv("CLIENT_ID", default="0")
    secret = getenv("CLIENT_SECRET", default="0")
    base_folder_id = getenv("BASE_FOLDER_ID", default="0")
    auth = OAuth2(
        client_id=id,
        client_secret=secret,
        access_token=token,
    )
    client = Client(auth)

    def items_in_folder(self, folder_id=base_folder_id):
        items = self.client.folder(folder_id=folder_id).get_items()
        files = []
        folders = []
        for item in items:
            dtc = {
                "id": item.id,
                "name": item.name,
                "type": item.type
            }
            if item.type == "file":
                files.append(dtc)
            else:
                folders.append(dtc)
        return files, folders

    def get_file_info(self, file_id):
        file_info = self.client.file(file_id).get()
        dtc = {
            "id": file_id,
            "name": file_info.name,
            "ext": file_info.name[-3:],
            "path": "/".join(s.name for s in file_info.path_collection['entries']) + f"/{file_info.name}",
            "parent_folder": {
                "id": file_info.path_collection['entries'][-1].id,
                "name": file_info.path_collection['entries'][-1].name,
                "url": "https://app.box.com/folder/" + file_info.path_collection['entries'][-1].id,
            },
            "url": "https://app.box.com/file/" + file_id
        }
        return dtc

    def get_thumbnail(self, file_id):
        return self.client.file(file_id).get_thumbnail_representation('92x92', extension='jpg')

    def download_file(self, file_id: str) -> [bytes, None]:
        info = self.get_file_info(file_id)
        if info['ext'] == 'pdf':
            cont = self.client.file(file_id).content()
            return cont


if __name__ == '__main__':
    box = BoxWrapper()
    inf = box.get_file_info("873662819506")
    for key, val in inf.items():
        print(f"{key} : {val}")
    # items_fold = box.items_in_folder("129133191949")
    # print(items_fold)
    # for item in items_fold:
    #     print(f"ID: {item.id}, name: {item.name}, type: {item.type}")
    # items_in_fold = list(box.items_in_folder())
    # fold = items_in_fold[0]
    # items_in_fold = list(box.items_in_folder(fold.id))
    # file_path, bts = box.download_file(23470514533)
    # print(file_path)
    # print(len(bts))
