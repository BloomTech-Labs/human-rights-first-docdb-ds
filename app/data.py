"""
Labs DS Data Engineer Role
- Database Interface
- Visualization Interface
"""
from os import getenv
from typing import Iterator, Dict, Iterable, Optional

from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv


class Data:
    """ MongoDB Data Model """
    load_dotenv()
    db_url = getenv("DB_URL", default="mongodb://localhost:27017/")
    db_name = getenv("DB_NAME", default="DocDB")
    db_table = getenv("DB_TABLE", default="docs")

    def connect(self):
        return MongoClient(self.db_url)[self.db_name][self.db_table]

    def find(self, query: Dict, projection: Dict = None) -> Iterator[Dict]:
        return self.connect().find(query, projection or {"_id": False})

    def find_one(self, query: Dict, projection: dict = None) -> Optional[Dict]:
        return self.connect().find_one(query, projection or {"_id": False})

    def insert_many(self, data: Iterable[Dict]):
        self.connect().insert_many(data)

    def insert(self, data: Dict):
        self.connect().insert_one(data)

    def update(self, query: Dict, data_update: Dict):
        self.connect().update_one(query, {"$set": data_update})

    def delete(self, query: Dict):
        self.connect().delete_many(query)

    def df(self) -> pd.DataFrame:
        return pd.DataFrame(self.find({}))

    def count(self, query: Dict) -> int:
        return self.connect().count_documents(query)

    def search(self, search: str, projection: dict = None):
        return self.find({"$text": {"$search": search}}, projection)

    def __str__(self):
        return f"{self.df()}"

    def create_index(self):
        self.connect().create_index([("$**", "text")])

    def delete_index(self):
        self.connect().drop_index("$**_text")

    def reset_db(self):
        self.delete({})
        self.delete_index()
        self.create_index()


# if __name__ == '__main__':
#     db = Data()
#     db.reset_db()
