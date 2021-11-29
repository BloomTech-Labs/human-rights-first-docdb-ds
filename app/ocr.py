import re
import pytesseract
from pdf2image import convert_from_bytes
import pandas as pd


def ocr(bts: bytes, dpi=90) -> str:
    pages = convert_from_bytes(bts, dpi=dpi)
    text = " ".join(map(pytesseract.image_to_string, pages))
    clean_text = re.sub(r"\s+", " ", text)
    return clean_text

def ocr_conf_mean(bts: bytes, dpi=150):
    """
    Convert pdf to document words and mean tesseract confidence.
    Argument: 1) bts (bytestring): pdf byte string, output from BoxWrapper.download_file(file_id)
              2) dpi (int): sets resolution of image converted from pdfs

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

    # make string from column of words
    out_str = " ".join(data_df['text'].tolist())

    return out_str, conf_mean


if __name__ == '__main__':
    from app.box_wrapper import BoxWrapper

    box = BoxWrapper()
    file_id = "23470520869"
    print(ocr(box.download_file(file_id), 300))
