from gensim.summarization.summarizer import summarize

from app.data import Data
from app.keywords import get_keywords


def summary(text: str, word_count: int) -> str:
    return summarize(text, word_count=word_count).replace("\n", " ").strip()


if __name__ == '__main__':
    db = Data()
    data = db.find({"$text": {"$search": "rubber bullets"}})[:10]

    for d in data:
        print(f"\nBox_id: {d['box_id']}")
        print(f"Old Path: {d['path']}")
        print(f"New Path: {'/'.join(d['path'].split('/')[2:])}")
        print(f"Summary: {summary(d['text'], word_count=150)}")
