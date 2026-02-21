class User:
    def __init__(self, username, path: str):
        from lifts import Lift
        self.username = username
        self.data = Lift(path)

    def get_lifts(self) -> list:
        return list(self.data.get_lifts())

    def lift_exists(self, lift: str) -> bool:
        if lift in self.data.get_lifts():
            return True
        return False

    def add_data(self, data: dict[str, str]) -> None:
        lift_name = data.pop("lift")
        self.data.add_data(lift_name, self.username, data)

    def lift_history(self, lift: str) -> list:
        return self.data.get_history(lift, self.username)
