"""
This is a series of functions that take in a jpg or pdf, runs it through tessaract
ocr, extracting words and confidence levels per word, then filters out words
below a specified confidence level.
"""

from PIL import Image
import pytesseract
import pdf2image
import time
import re
import pandas as pd


def tesseractor(image_name):
    """
    Convert a document image to a list of document words with associated data.

    Argument: A path to an image.
    Returns: A list of tab seperated value strings representing rows from
    the output of pytesseract.image_to_data().
    """
#     #timer for testing
#     start_time=time.time()
    if re.search(r'.jpg?', image_name):
        # jpg handler
        with Image.open(image_name) as im:
            str_list = pytesseract.image_to_data(im).split('\n')[:-1]

    else:
        # pdf handler
        pages = pdf2image.convert_from_bytes(open(image_name, 'rb').read())

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

#         #timer for testing
#         end_time=time.time()-start_time
#         print('execution time: ', end_time, 'seconds')
    return str_list


def filter_by_confidence(str_list, conf_threshold):
    """
    Drop words below a given confidence threshold.

    Arguments:
        1) A list of tab-seperated value strings, output by tesseract.
        2) kwarg, A Confidence threshold [0-100], below which words are dropped.
    Returns: A string of words with words below conf_threshold ommited.
    """
    # split-out elements
    data_df = pd.DataFrame([x.split('\t') for x in str_list])
    # set first line as column names
    data_df.columns = data_df.iloc[0]
    # drop first row: names, drop last row: all none
    data_df = data_df.iloc[1:]
    # convert confidence values to int for mean(), filtering
    data_df['conf'] = data_df['conf'].astype('int')

#     conf_mean = data_df['conf'].mean()
    # drop rows with conf < threshold, drop white-space words
    conf_df = data_df.loc[data_df['conf'] >= conf_threshold]
    conf_df = conf_df.loc[conf_df['text'].str.contains('[^\s+]')]
    # return a string of words leftover
    return " ".join(conf_df['text'].tolist())


def tess_and_filter(image_name, conf_threshold=50, print_timer=False):
    """Compose above two functions. Optional timer for speed testing."""
    start_time = time.time()
    word_string = filter_by_confidence(tesseractor(image_name), conf_threshold)
    end_time = time.time()-start_time
    if print_timer is True:
        print('execution time: ', end_time, 'seconds')
    return word_string
