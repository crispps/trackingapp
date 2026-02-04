import json


class Lift:
    def __init__(self):
        self.path = "data/lifts.json"
        with open(self.path, "r") as f:
            self.data = json.load(f)
            f.close()

    def add_data(self, user: str, lift: str, date: str, weight: str, sets: str, reps: str, rpe: str):
        if user not in self.data[lift]:
            self.data[lift][user] = []
        self.data[lift][user].append({"date": date, "weight": weight, "sets": sets, "reps": reps, "rpe": rpe})
        self.dump_data()

    def dump_data(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f)
            f.close()

    def update_data(self):
        with open(self.path, "r") as f:
            self.data = json.load(f)
            f.close()

    def add_lift(self, lift: str) -> None:
            self.data[lift] = {}
            self.dump_data()

    def get_lifts(self) -> list:
        return list(self.data.keys())

    def get_history(self, lift: str, user: str) -> list:
        return self.data[lift][user]