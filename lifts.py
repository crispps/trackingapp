import json


class Lift:
    def __init__(self):
        self.path = "data/lifts.json"
        with open(self.path, "r") as f:
            self.data = json.load(f)
            f.close()

    def add_data(self, lift_name: str, user: str, data: dict[str, str]) -> None:
        if user not in self.data[lift_name]:
            self.data[lift_name][user] = []
        self.data[lift_name][user].append(data)
        self.dump_data()

    def dump_data(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f)
            f.close()

    def add_lift(self, lift: str) -> bool:
        exists = False
        for key in list(self.data.keys()):
            if lift == key:
                exists = True
        if not exists:
            self.data[lift] = {}
            self.dump_data()
        return exists

    def get_lifts(self) -> list:
        return list(self.data.keys())

    def get_history(self, lift: str, user: str) -> list:
        return self.data[lift][user]


