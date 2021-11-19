from dotenv import load_dotenv
from os import getenv
from boxsdk import OAuth2, Client


base_folder_id = getenv("BASE_FOLDER_ID", default="855631806")


class BoxWrapper:
    load_dotenv()
    auth = OAuth2(
        client_id=getenv("CLIENT_ID"),
        client_secret=getenv("CLIENT_SECRET"),
        access_token=getenv("DEV_TOKEN"),
    )
    client = Client(auth)

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
        path = "/".join(s.name for s in file_info.path_collection['entries'])
        dtc = {
            "id": file_id,
            "name": file_info.name,
            "ext": file_info.name.split(".")[-1],
            "path": f"{path}/{file_info.name}",
            "url": f"https://app.box.com/file/{file_id}",
        }
        return dtc

    def get_thumbnail(self, file_id):
        """ sizes of 32x32, 94x94, 160x160, 320x320 """
        file_handle = self.client.file(file_id)
        return file_handle.get_thumbnail_representation('320x320', extension='jpg')

    def download_file(self, file_id: str) -> [bytes, None]:
        info = self.get_file_info(file_id)
        if info['ext'] == 'pdf':
            cont = self.client.file(file_id).content()
            return cont
