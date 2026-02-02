import json


class Lift:
    def __init__(self, name: str):
        self.name = name

    def add_data(self, user: str, date: str, weight: int, reps: int, rpe: int) -> None:
        with open("lifts.json", "r") as f:
            lifts = json.load(f)
            f.close()
        lifts[self.name][user].append({"date": date, "weight": weight, "reps": reps, "rpe": rpe})
        with open("lifts.json", "w") as f: