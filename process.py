import json
import tui
from user import User

user: object


# returns bool if login already exists
def check_login(username: str) -> bool:
    with open("data/users.json", "r") as f:
        users = json.load(f)
    for i in users:
        if username == i:
            return True
    return False


def login(username: str) -> bool:
    global user
    logged_in = False
    if not logged_in:
        logged_in = check_login(username)

    user = User(username)

    return logged_in


def create_user(username: str) -> bool:
    username_available = False
    with open("data/users.json", "r") as f:
        users = json.load(f)
        f.close()
    if not username_available:
        username_available = not check_login(username)
        if not username_available:
            return False
    with open("data/users.json", "w") as f:
        users.append(username)
        json.dump(users, f)
        f.close()
    return True


def submit_lift_data() -> None:
    lift_exists = False
    while not lift_exists:
        data = tui.get_lift_data()
        lift_exists = user.lift_exists(data[0])
        if not lift_exists:
            tui.lift_doesnt_exist()
    user.add_data(data)


def lift_history() -> None:
    lift_exists = False
    while not lift_exists:
        data = tui.get_lift()
        lift_exists = user.lift_exists(data)
        if not lift_exists:
            tui.lift_doesnt_exist()
    lift_history = user.lift_history(data)
    tui.display_history(lift_history)

