import json
from os import getenv
from typing import Iterator, Dict, Optional, Iterable

from pymongo import MongoClient
from dotenv import load_dotenv


class MongoDB:
    """ MongoDB Data Model """
    load_dotenv()

    def connect(self):
        return MongoClient(
            getenv("DB_URL")
        )[getenv("DB_NAME")][getenv("DB_TABLE")]

    def search(self, search: str):
        return self.connect().find(
            {"$text": {"$search": search}},
            {"_id": False, "text": False},
        )

    def find(self, query: Dict) -> Iterator[Dict]:
        return self.connect().find(query, {"_id": False})

    def find_one(self, query: Dict) -> Optional[Dict]:
        return self.connect().find_one(query, {"_id": False})

    def find_all(self):
        return self.connect().find({}, {"_id": False})

    def count(self, query: Dict):
        return self.connect().count_documents(query)

    def insert(self, data: Dict):
        self.connect().insert_one(data)

    def insert_many(self, data: Iterable[Dict]):
        self.connect().insert_many(data)

    def update(self, query: Dict, data_update: Dict):
        self.connect().update_one(query, {"$set": data_update})

    def delete(self, query: Dict):
        self.connect().delete_many(query)

    def push_list(self, query: Dict, list_name, value):
        self.connect().update(query, {'$push': {list_name: value}})

    def pull_list(self, query: Dict, list_name, value):
        self.connect().update(query, {'$pull': {list_name: value}})

    def backup(self, file_name):
        data = list(self.find_all())
        with open(file_name, "w") as file:
            json.dump(data, file)

    def restore(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
        self.insert_many(data)
