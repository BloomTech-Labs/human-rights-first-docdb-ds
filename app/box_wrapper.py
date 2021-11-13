from dotenv import load_dotenv
from os import getenv
from boxsdk import OAuth2, Client


class BoxWrapper:
    load_dotenv()
    auth = OAuth2(
        client_id=getenv("CLIENT_ID"),
        client_secret=getenv("CLIENT_SECRET"),
        access_token=getenv("DEVELOPER_TOKEN"),
    )
    client = Client(auth)
    base_folder_id = getenv("BASE_FOLDER_ID", default="855631806")

    def items_in_folder(self, folder_id: str = base_folder_id):
        items = self.client.folder(folder_id).get_items()
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

    def get_file_info(self, file_id: str):
        file_info = self.client.file(file_id).get()
        dtc = {
            "id": file_id,
            "name": file_info.name,
            "ext": file_info.name.split(".")[-1],
            "path": "/".join(s.name for s in file_info.path_collection['entries']) + f"/{file_info.name}",
            "url": f"https://app.box.com/file/{file_id}",
            "size": file_info.size,
        }
        return dtc

    def get_thumbnail(self, file_id):
        """ sizes of 32x32, 94x94, 160x160, 320x320 """
        return self.client.file(file_id).get_thumbnail_representation('94x94', extension='jpg')

    def download_file(self, file_id: str) -> [bytes, None]:
        info = self.get_file_info(file_id)
        if info['ext'] == 'pdf':
            cont = self.client.file(file_id).content()
            return cont


if __name__ == '__main__':
    box = BoxWrapper()
    # "Folder with only files in it:"
    # files1, folds1 = box.items_in_folder("2757280923")
    # for item in files1:
    #     for key, val in item.items():
    #         print(f"{key} : {val}")
    # print("For reference, here's the list of folders in the folder")
    # print(folds1)
    # print()

    # print("Folder with only folders in it:")
    # files2, folds2 = box.items_in_folder("129133191949")
    # for item in folds2:
    #     for key, val in item.items():
    #         print(f"{key} : {val}")
    # print("For reference, here's the list of files in the folder")
    # print(files2)
    # print()

    print("File Info:")
    inf = box.get_file_info("23470520869")
    print(inf)
    # for key, val in inf.items():
    #     if isinstance(val, dict):
    #         print(key + ": {")
    #         for k, v in val.items():
    #             print(f"    {k} : {v}")
    #         print("}")
    #     else:
    #         print(f"{key} : {val}")
    # print()

    # print("Download file:")
    # bts = box.download_file("23470520869")
    # print(f"Length: {len(bts)}")
    # print(f"Type: {type(bts)}")
