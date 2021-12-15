from app.data import Data
from app.keywords import get_keywords
from app.summary import summary


db = Data()
data = db.find({"box_id": "23470520869"})

# for d in data:
#     db.update(
#         {"box_id": d["box_id"]},
#         {"tags": get_keywords(d["text"], max_ngram=5, n_keywords=5)},
#     )
#     print(d['box_id'])


# for d in data:
#     text = d["text"]
#     db.update(
#         {"box_id": d["box_id"]},
#         {"summary": summary(text, word_count=150)},
#     )


# for d in data:
#     db.update(
#         {"box_id": d["box_id"]},
#         {"path": "/".join(d["path"].split("/")[2:])},
#     )


for d in data:
    print(summary(d["text"], 150))
