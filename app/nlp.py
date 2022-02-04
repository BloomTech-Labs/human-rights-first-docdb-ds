from typing import List

import yake

from app.box_wrapper import BoxWrapper
from app.ocr import ocr


def get_tags(text: str) -> List[str]:
    language = "en"
    max_ngram_size = 5
    deduplication_threshold = 0.3
    num_keywords = 7
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size,
                                                dedupLim=deduplication_threshold, top=num_keywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    return [s[0] for s in sorted(keywords, key=lambda s: s[1])]


if __name__ == '__main__':
    box = BoxWrapper()
    file_id = "23470520869"
    raw_text = ocr(box.download_file(file_id), 300)
    print(get_tags(raw_text))