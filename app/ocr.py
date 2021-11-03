import re
import pytesseract
from pdf2image import convert_from_bytes


class DocProcessor:
    def get_text(self, bts: bytes, dpi=90):
        pages = convert_from_bytes(bts, dpi=dpi)
        text = " ".join(map(pytesseract.image_to_string, pages))
        clean_text = re.sub(r"\s+", " ", text)
        return clean_text


if __name__ == '__main__':
    from .box_wrapper import BoxWrapper

    box = BoxWrapper()
    file_id = "23470520869"
    info = box.get_file_info(file_id)
    doc_processor = DocProcessor()
    info['text'] = doc_processor.get_text(box.download_file(file_id), 200)
    for key, val in info.items():
        if key == "text":
            print(f"{key} : {val[:200]}")
        else:
            print(f"{key} : {val}")
