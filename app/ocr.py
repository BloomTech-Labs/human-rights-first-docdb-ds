import re
import pytesseract
from pdf2image import convert_from_bytes
import pandas as pd
import time


def ocr(bts: bytes, dpi=90) -> str:
    pages = convert_from_bytes(bts, dpi=dpi)
    text = " ".join(map(pytesseract.image_to_string, pages))
    clean_text = re.sub(r"\s+", " ", text)
    return clean_text

def ocr_conf_mean(bts: bytes, dpi=150):
    """
    Convert pdf to document words and mean tesseract confidence.
    Argument: 1) bts (bytestring): Byte string, output from BoxWrapper.download_file(file_id)
              2) dpi (int): integer, sets resolution of image converted from pdfs

    Returns: A tuple containing:
        1) str: String of unformated document words
        2) float: Mean of document word confidences
    """
    # pdf handler
    pages = convert_from_bytes(bts, dpi=dpi)

    str_list = []
    for i in range(len(pages)):
        # for multi-page pdfs: concatenate each pages data to one list
        page_data = pytesseract.image_to_data(pages[i])
        if i == 0:
            # keep the column names on the first page
            str_list = str_list + page_data.split('\n')[:-1]
        else:
            # drop column names on subsequent pages
            str_list = str_list + page_data.split('\n')[1:-1]

    # split-out elements
    data_df = pd.DataFrame([x.split('\t') for x in str_list])
    # set first line as column names
    data_df.columns = data_df.iloc[0]
    # drop first row: names,
    data_df = data_df.iloc[1:]
    data_df = data_df[['text', 'conf']]
    # convert confidence values to int for mean(), filtering
    data_df['conf'] = data_df['conf'].astype('int')
    # get mean
    conf_mean = data_df['conf'].mean()
    # print('CONF_MEAN: ', conf_mean) # for test

    # make string from column of words
    out_str = " ".join(data_df['text'].tolist())

    return out_str, conf_mean




if __name__ == '__main__':
    from app.box_wrapper import BoxWrapper

    box = BoxWrapper()
    #legible, straight, typwritten doc. Mean confidence: 70%. 9% time overhead with Mean_confidence
    # file_id = "23470520869"
    #news paper clippings, bad photos. Mean confidence: 59%. 6% time overhead with Mean_confidence
    # file_id = "305364848415".
    #crude map with some text and labels. Mean_confidence: 29%. 1% time overhead with Mean_confidence
    # file_id = "17742201678"
    #side_ways tabular docs. Mean_confidence: 19%. 1% time overhead with Mean_confidence
    file_id = "8281189693"

    pdf_bytes = box.download_file(file_id)

    s = time.time()
    ocr_conf_mean(pdf_bytes, 300)
    print('with confidence:', time.time() - s)

    s = time.time()
    ocr(pdf_bytes, 300)
    print('without confidence:', time.time() - s)

    # info = box.get_file_info(file_id)
    # info['text'] = ocr(box.download_file(file_id), 200)
    # for key, val in info.items():
    #     if key == "text":
    #         print(f"{key} : {val[:200]}")
    #     else:
    #         if isinstance(val, dict):
    #             print(key + ": {")
    #             for k, v in val.items():
    #                 print(f"    {k} : {v}")
    #             print("}")
    #         else:
    #             print(f"{key} : {val}")
