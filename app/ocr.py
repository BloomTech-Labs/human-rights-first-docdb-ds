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
    from nlp import keyword_extraction
    box = BoxWrapper()
    file_id = "23470520869"
    info = box.get_file_info(file_id)
    info['text'] = ocr(box.download_file(file_id), 200)
    for key, val in info.items():
        if key == "text":
            print(f"{key} : {val[:]}")
            print(f"Keywords: {keyword_extraction(info['text'])}")
        else:
            if isinstance(val, dict):
                print(key + ": {")
                for k, v in val.items():
                    print(f"    {k} : {v}")
                print("}")
            else:
                print(f"{key} : {val}")
