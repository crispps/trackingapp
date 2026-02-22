import json


class Lift:
    def __init__(self, path: str):
        self.path = path
        self.data = self.load_lift_data()

    def load_lift_data(self) -> str:
        with open(self.path, "r") as f:
            data = json.load(f)
            f.close()
        return data

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
        self.data[lift] = {}
        self.dump_data()

    def get_lifts(self) -> list:
        return list(self.data.keys())

    def get_history(self, lift: str, user: str) -> str:
        return self.data[lift][user]


