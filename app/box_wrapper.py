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
        return self.client.folder(folder_id=folder_id).get_items()

    def get_file_info(self, file_id):
        file_info = self.client.file(file_id).get()
        return file_info

    def get_thumbnail(self, file_id):
        return self.client.file(file_id).get_thumbnail_representation('92x92', extension='jpg')

    def download_file(self, file_id: str) -> Union[Tuple[str, bytes], None]:
        info = self.get_file_info(file_id)
        pth = "/".join(s.name for s in info.path_collection['entries']) + f"/{info.name}"
        if info.name[-3:] == 'pdf':
            cont = self.client.file(file_id).content()
            return pth, cont


if __name__ == '__main__':
    box = BoxWrapper()
    items_in_fold = list(box.items_in_folder())
    fold = items_in_fold[0]
    items_in_fold = list(box.items_in_folder(fold.id))
    file_path, bts = box.download_file(items_in_fold[0].id)
    print(file_path)
    print(len(bts))
