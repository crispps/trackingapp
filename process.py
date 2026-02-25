import json
import tui
from user import User
from database import Database

user: object


def get_database_path() -> str:
    return "data/trackingapp.db"


db = Database(get_database_path())
db.connect()


def get_users_path() -> str:
    path = "data/users.json"
    return path


def get_data_path() -> str:
    path = "data/lifts.json"
    return path


def get_user_list() -> list:
    print("get_user_list")
    result = db.fetchall("SELECT username FROM users")
    user_list = []
    for i in result:
        user_list.append(i["username"])
    return user_list


def check_username_exists(username: str) -> bool:
    users = get_user_list()
    for i in users:
        if username == i:
            return True
    return False


def login(username: str) -> bool:
    global user
    logged_in = check_username_exists(username)
    if logged_in:
        user = User(username, get_database_path())
    else:
        user = None
    db.disconnect()
    return logged_in


def add_user_to_file(username: str) -> None:

    db.execute("INSERT INTO users (username) VALUES (?)", (username,))


def create_user(username: str) -> bool:
    if check_username_exists(username):
        return False
    add_user_to_file(username)
    return True


def submit_lift_data(data: dict[str, str]) -> None:
    user.add_data(data)


# not fixed for gui
def lift_history(lift_name) -> list:
    lift_history = user.lift_history(lift_name)
    return list(lift_history)


def new_lift(lift_name) -> bool:
    return user.add_lift(lift_name)
