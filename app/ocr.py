import re
import pytesseract
from pdf2image import convert_from_bytes
import pandas as pd


def ocr(bts: bytes, dpi=90) -> str:
    pages = convert_from_bytes(bts, dpi=dpi)
    text = " ".join(map(pytesseract.image_to_string, pages))
    clean_text = re.sub(r"\s+", " ", text)
    return clean_text

def ocr_conf_flag(bts: bytes, dpi=90, conf_threshold=30):
    """
    Convert pdf to document words and flag for low confidence documents.
    Argument: 1) Byte string, output from BoxWrapper.download_file(file_id)
              2) dpi: integer, sets resolution of image converted from pdfs
              3) conf_threshold: integer, determines level of document confidence under which to set conf_flag

    Returns: Document words, a flag if document confidence is less than conf_threshold
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
    # set confidence flag
    conf_flag =  conf_mean < conf_threshold
    # make string from column of words
    out_str = " ".join(data_df['text'].tolist())

    return out_str, conf_flag




if __name__ == '__main__':
    from app.box_wrapper import BoxWrapper

    box = BoxWrapper()
    # file_id = "23470520869" #legible, straight, typwritten doc. Mean confidence: 70%
    # file_id = "305364848415" #news paper clippings, bad photos. Mean confidence: 59%
    # file_id = "17742201678" #crude map with some text and labels. Mean_confidence: 29%
    file_id = "8281189693" #side_ways tabular docs: 19%

    pdf_bytes = box.download_file(file_id)

    print(ocr_conf_flag(pdf_bytes, 300, 40))

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
