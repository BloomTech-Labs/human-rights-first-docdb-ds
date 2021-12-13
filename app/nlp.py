from typing import List

import requests
import spacy
import pytextrank


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
    file_ids = ["23470520869", "455229161973"]
    for file_id in file_ids:
        result = requests.get(f"https://ds.humanrightsfirstdocdb.dev/lookup/{file_id}")
        raw_text = result.json()["Response"]["text"]
        # print(raw_text)
        print(get_tags(raw_text))
