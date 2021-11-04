import re
import pytesseract
from pdf2image import convert_from_bytes
from app.box_wrapper import BoxWrapper


def make_fields(fold_id: str, file_id: str):
    box = BoxWrapper()
    file_path, bts = box.download_file(file_id)
    pages = convert_from_bytes(bts, dpi=90)
    text = " ".join(map(pytesseract.image_to_string, pages))
    clean_text = re.sub(r"\s+", " ", text)
    doc_data = DocProcessor(fold_id, file_id, file_path, clean_text).create_dict()
    return doc_data


class DocProcessor:
    def __init__(self, fold_id: str, file_id: str, file_path: str, clean_txt: str):
        self.fold_id = fold_id
        self.file_id = file_id
        self.file_path = file_path
        self.clean_text = clean_txt
        self.box = BoxWrapper()

    def get_item(self):
        return list(self.box.items_in_folder(self.fold_id))

    def file_name(self):
        lst = list(self.box.items_in_folder(self.fold_id))
        file_name = [item.name for item in lst if item.id == self.file_id]
        return file_name[0]

    def create_dict(self):
        return {
            'folder_id': self.fold_id,
            'file_id': self.file_id,
            'file_name': self.file_name(),
            'file_path': self.file_path,
            'text': self.clean_text,

        }

#enter folder_id and file_id in this order:
#make_fields(folder_id,file_id)
#print(make_fields('47390913460', '76914476897'))
