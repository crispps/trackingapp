import json
import sqlite3
from sqlite3 import Connection

from database import Database


class Lift:
    def __init__(self, path: str):
        self.path = path
        self.data = self.load_lift_data()

    def load_lift_data(self) -> object:
        db = Database(self.path)
        db.connect()
        return db

    def add_data(self, lift_name: str, user: str, data: dict[str, str]) -> None:
        if user not in self.data[lift_name]:
            self.data[lift_name][user] = []
        self.data[lift_name][user].append(data)
        self.dump_data()

    def dump_data(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f)
            f.close()

    def add_lift(self, lift: str) -> None:
        self.data.fetchall("INSERT INTO lifttype VALUES (lift) ")

    def get_lifts(self) -> list:
        lifts = self.data.fetchall("SELECT name FROM lifttype")
        existing_lifts = []
        for i in lifts:
            existing_lifts.append(i["name"])
        return existing_lifts

    def get_history(self, lift: str, user: str):
        return self.data[lift][user]


