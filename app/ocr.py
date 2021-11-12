import re
import pytesseract
from pdf2image import convert_from_bytes


def ocr(bts: bytes, dpi=90) -> str:
    pages = convert_from_bytes(bts, dpi=dpi)
    text = " ".join(map(pytesseract.image_to_string, pages))
    clean_text = re.sub(r"\s+", " ", text)
    return clean_text


if __name__ == '__main__':
    from app.box_wrapper import BoxWrapper

    box = BoxWrapper()
    file_id = "23470520869"
    print(ocr(box.download_file(file_id), 200))
