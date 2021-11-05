import spacy

nlp = spacy.load("en_core_web_sm")


def get_entities(text):
    """Get tags from text using SpaCy NER"""
    doc = nlp(text)
    return [e.text for e in doc.ents]


if __name__ == '__main__':
    s = "This is some text with a name in it: Robert Sharp"
    print(get_entities(s))
