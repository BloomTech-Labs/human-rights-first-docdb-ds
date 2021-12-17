from gensim.summarization.summarizer import summarize

from app.data import Data


def summary(text: str, word_count: int = 150) -> str:
    error_text = "No Summary Available"
    try:
        output = summarize(
            text,
            word_count=word_count,
        ).replace("\n", " ").strip()
        return output or error_text
    except ValueError:
        return error_text


if __name__ == '__main__':
    db = Data()
    # for idx, d in enumerate(db.find_all(), 1):
    #     db.update({"box_id": d["box_id"]}, {"summary": summary(d["text"])})
    #     print(f"{idx}: {d['box_id']}")
    print(db.count({"summary": "No Summary Available"}))
