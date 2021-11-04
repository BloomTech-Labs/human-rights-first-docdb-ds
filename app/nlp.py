import spacy
nlp = spacy.load("en_core_web_md")

def get_tags(text):
    """Get tags from text using SpaCy NER"""

    doc = nlp(text)

    tags = [e.text for e in doc.ents]

    return tags
