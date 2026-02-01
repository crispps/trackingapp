import json
import tui as ui

user: str


def signup(path) -> bool:
    with open(path, "r") as f:
        users = json.load(f)
        f.close()
    user_created = False
    while not user_created:
        username = ui.get_username()
        if username not in users:
            users.append(username)
            with open(path, "w") as f:
                json.dump(users, f)
                f.close()
            user_created = True
    return user_created


def login(path, username) -> bool:
    logged_in = False
    with open(path, "r") as f:
        users = json.load(f)
    while not logged_in:
        for user in users:
            if user == username:
                logged_in = True
        return logged_in

