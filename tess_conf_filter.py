"""
This is a series of functions that take in a pdf, runs it through tessaract
OCR, extracting words and confidence levels per word, then filters out words
below a specified confidence level.
"""

import pytesseract
import pdf2image
import pandas as pd


def tesseractor(byte_string):
    """
    Convert a document image to a list of document words with associated data.

    Argument: A path to an image.
    Returns: A list of tab seperated value strings representing rows from
    the output of pytesseract.image_to_data().
    """
    # pdf handler
    pages = pdf2image.convert_from_bytes(byte_string)

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


def tess_and_filter(bts, conf_threshold=50, return_conf_mean=False):
    """
    tesseractor() then filter_by_confidence.

    Arguments:
        1) A byte_string from box_wrapper.download_file()
        2) (kwarg) An integer [0-100], representing a percent
            word-confidence-threshold, below which words are dropped
        3) (kwarg) if True: returns the mean of word-confidence values of
            tesseract converted document as a second value.

    Returns:
        A tuple of a tessearact produced string and word_confidence mean
        value, when return_conf_mean=True
    """
    word_string = filter_by_confidence(tesseractor(bts), conf_threshold, return_conf_mean)
    return (word_string)
