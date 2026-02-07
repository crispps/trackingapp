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


def login() -> bool:
    global user
    logged_in = False
    username = ""
    while not logged_in:
        username = tui.get_username()
        logged_in = check_login(username)
        if not logged_in:
            tui.login_failed()
    user = User(username)

    return logged_in


def create_user() -> None:
    username_available = False
    username = ""
    with open("data/users.json", "r") as f:
        users = json.load(f)
        f.close()
    while not username_available:
        username = tui.get_username()
        username_available = not check_login(username)
        if not username_available:
            tui.username_unavailble()
    with open("data/users.json", "w") as f:
        users.append(username)
        json.dump(users, f)
        f.close()
    tui.user_created()


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

