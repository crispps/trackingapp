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
    db.connect()
    result = db.fetchall("SELECT username FROM users")
    db.disconnect()
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
    db.connect()
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


def create_block(block_type, block_name) -> bool:
    return user.create_block(block_type, block_name)


def submit_lift_data(data: dict[str, str]) -> None:
    user.add_data(data)


def bubblesort(data: list, sort_by: str) -> list:
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i][sort_by] > data[j][sort_by]:
                data[i], data[j] = data[j], data[i]
    return data


def get_lift_history(lift_name, block_name, order_by) -> tuple:
    lift_history = user.lift_history(lift_name, block_name)
    # if order_by == "Weight":
    #     lift_history = bubblesort(lift_history, "weight")
    return lift_history


def new_lift(lift_name) -> bool:
    return user.add_lift(lift_name)


def get_blocks() -> list:
    result = user.get_blocks()
    return [row["name"] for row in result]


def check_date_format(data) -> bool:
    from datetime import datetime
    date_format = "%Y-%m-%d"
    try:
        res = bool(datetime.strptime(data, date_format))
    except ValueError:
        res = False
    return res


def check_if_float(data) -> bool:
    if data is None:
        return False
    try:
        float(data)
        return True
    except ValueError:
        return False


def check_if_int(data) -> bool:
    if data is None:
        return False
    try:
        int(data)
        return True
    except ValueError:
        return False


def format_data_by_week(data: tuple) -> list[str]:
    print(data)
    history = data[0]
    display_type = data[1]
    print(display_type)
    weeks_range = get_week_ranges(data)
    formatted_data = []
    for week_num, i in enumerate(weeks_range, start=1):
        formatted_data.append("separator")
        formatted_data.append(f"Week {week_num}: {i[0]} - {i[1]}")
        formatted_data.append("separator")
        count = 0
        dates_done = []
        for entry in history:
            if i[0] <= entry["date"] <= i[1]:
                if entry["date"] not in dates_done:
                    dates_done.append(entry["date"])
                    count += 1
                    formatted_data.append(f"Day {count} - {entry['date']}:")
                formatted_data.append(f"{entry['liftname']} - {entry['weight']}kg - {entry['sets']}x{entry['reps']} - "
                                      f"@{entry['rpe']}")
    return formatted_data


def get_week_ranges(data: tuple) -> list[tuple]:
    from datetime import datetime, timedelta
    history = data[0]
    display_type = data[1]
    weeks_range = []
    if display_type == "All lifts":
        for entry in history:
            dt = datetime.strptime(entry["date"], "%Y-%m-%d")
            if not weeks_range or not (weeks_range[-1][0] <= entry["date"] <= weeks_range[-1][1]):
                week_start = dt - timedelta(days=dt.weekday())
                week_end = week_start + timedelta(days=6)
                weeks_range.append((week_start.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d")))
    return weeks_range
