class User:
    def __init__(self, username):
        from lifts import Lift
        self.username = username
        self.data = Lift()

    def get_lifts(self) -> list:
        return list(self.data.get_lifts())

    def lift_exists(self, lift: str) -> bool:
        if lift in self.data.get_lifts():
            return True
        return False

    def add_data(self, data: tuple) -> None:
        self.data.add_data(self.username, data[0], data[1], data[2], data[3], data[4], data[5])

    def lift_history(self, lift: str) -> list:
        return self.data.get_history(lift, self.username)
