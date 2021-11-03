import re
import pytesseract
from pdf2image import convert_from_bytes
import pandas as pd


class DocProcessor:
    def get_text(self, bts: bytes, dpi=90):
        pages = convert_from_bytes(bts, dpi=dpi)
        text = " ".join(map(pytesseract.image_to_string, pages))
        clean_text = re.sub(r"\s+", " ", text)
        return clean_text

    def get_text_conf_filter(self, bts: bytes, dpi=90, conf_threshold=30, return_conf_mean=False):
        def tesseractor(byte_string):
            """
            Convert pdf to a list of document words with associated data.

            Argument: A byte_string.
            Returns: A list of tab seperated value strings representing rows from
            the output of pytesseract.image_to_data().
            """
            # pdf handler
            pages = convert_from_bytes(byte_string)

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

            return str_list


        def filter_by_confidence(str_list, conf_threshold, return_conf_mean=False):
            """
            Drop words below a given confidence threshold.

            Arguments:
                1) A list of tab-seperated value strings, output by tesseract.
                2) kwarg: A Confidence threshold [0-100], below which words are dropped.
                3) kwarg: Flag to return the document mean confidence
            Returns:
                1) A string of words with words below conf_threshold ommited.
                2) Optionally a document mean confidence value

            """
            # split-out elements
            data_df = pd.DataFrame([x.split('\t') for x in str_list])
            # set first line as column names
            data_df.columns = data_df.iloc[0]
            # drop first row: names,
            data_df = data_df.iloc[1:]
            data_df = data_df[['text', 'conf']]
            # convert confidence values to int for mean(), filtering
            data_df['conf'] = data_df['conf'].astype('int')

            conf_mean = data_df['conf'].mean()
            # drop rows with conf < threshold, drop white-space words
            conf_df = data_df.loc[data_df['conf'] >= conf_threshold]
            conf_df = conf_df.loc[conf_df['text'].str.contains('[^\s+]')]
            # return a string of words leftover
            out_str = " ".join(conf_df['text'].tolist())
            if return_conf_mean == False:
                return out_str
            else:
                return out_str, conf_mean

        return filter_by_confidence(tesseractor(bts), conf_threshold, return_conf_mean)


if __name__ == '__main__':
    from .box_wrapper import BoxWrapper

    box = BoxWrapper()
    file_id = "23470520869"
    info = box.get_file_info(file_id)
    doc_processor = DocProcessor()
    # info['text'] = doc_processor.get_text(box.download_file(file_id), 200)
    info['text'] = doc_processor.get_text_conf_filter(box.download_file(file_id),
                                                                        200,
                                                                        conf_threshold=60,
                                                                        return_conf_mean=False)
    for key, val in info.items():
        if key == "text":
            print(f"{key} : {val[:200]}")
        else:
            print(f"{key} : {val}")
