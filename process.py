import json
import tui
from user import User

user: object


def get_users_path() -> str:
    path = "data/users.json"
    return path


def get_data_path() -> str:
    path = "data/lifts.json"
    return path


def get_user_list() -> list:
    with open(get_users_path(), "r") as f:
        users = json.load(f)
        f.close()
    return users


def check_username_exists(username: str) -> bool:
    users = get_user_list()
    for i in users:
        if username == i:
            return True
    return False


# returns bool if login already exists
def check_login(username: str) -> bool:
    return check_username_exists(username)


def login(username: str) -> bool:
    global user
    logged_in = check_login(username)
    if logged_in:
        user = User(username, get_data_path())
    else:
        user = None
    return logged_in


def add_user_to_file(username: str) -> None:
    users = get_user_list()
    with open(get_users_path(), "w") as f:
        users.append(username)
        json.dump(users, f)
        f.close()


def create_user(username: str) -> bool:
    if check_username_exists(username):
        return False
    add_user_to_file(username)
    return True


def submit_lift_data(data: dict[str, str]) -> None:
    user.add_data(data)


# not fixed for gui
def lift_history() -> None:
    lift_exists = False
    while not lift_exists:
        data = tui.get_lift()
        lift_exists = user.lift_exists(data)
        if not lift_exists:
            tui.lift_doesnt_exist()
    lift_history = user.lift_history(data)
    tui.display_history(lift_history)
