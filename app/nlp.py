from typing import List

import spacy
import pytextrank

from app.box_wrapper import BoxWrapper
from app.ocr import ocr

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("positionrank")  # requires `import pytextrank`
custom_stopwords = {
    "page", "secret", "document", ":", ";", "_", "|", "/", "\\", "| |",
}
stopwords = nlp.Defaults.stop_words.union(custom_stopwords)


def get_tags(text: str) -> List[str]:
    doc = nlp(text)
    return [
        phrase.text for phrase in doc._.phrases[:20]
        if phrase.text.lower() not in stopwords
    ][:10]


if __name__ == '__main__':
    box = BoxWrapper()
    file_id = "23470520869"
    raw_text = ocr(box.download_file(file_id), 300)
    print(get_tags(raw_text))
