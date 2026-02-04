

def get_username() -> str:
    username = input("Enter username: ")
    return username.lower()


def login_success() -> None:
    print("Login successful")


def login_failed() -> None:
    print("Login failed")


def user_created() -> None:
    print("User created successfully")


def username_unavailble() -> None:
    print("Account already exists")


def lift_doesnt_exist() -> None:
    print("Lift doesn't exist")


def lift_exists() -> None:
    print("Lift already exists")


def titletext(title: str) -> None:
    print("-"*len(title))
    print(title)
    print("-"*len(title))


def start_menu() -> str:
    titletext("Welcome to trackingapp")
    option_selected = False
    choice = ""
    while not option_selected:
        print("1. Login")
        print("2. Create Account")
        choice = input("Enter your choice: ")
        if choice in ["1", "2"]:
            option_selected = True
        else:
            print("Invalid choice")
    return choice


def main_menu() -> str:
    option_selected = False
    choice = ""
    while not option_selected:
        print("1. Record lift")
        print("2. View lifts")
        print("3. Create new lift")
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3"]:
            option_selected = True
        else:
            print("Invalid choice")
    return choice


def get_lift_data() -> tuple:
    lift_name = input("Enter lift name: ")
    lift_date = input("Enter lift date (YYYY-MM-DD): ")
    lift_weight = input("Enter lift weight (kg): ")
    lift_sets = input("Enter lift sets: ")
    lift_reps = input("Enter lift reps: ")
    lift_rpe = input("Enter lift RPE: ")
    return lift_name, lift_date, lift_weight, lift_sets, lift_reps, lift_rpe


def get_lift() -> str:
    lift = input("Enter lift name: ")
    return lift


def display_history(history: list) -> None:
    print("Lift history:")
    for entry in history:
        print(f"{entry['date']} - {entry['weight']}kg - {entry['sets']}x{entry['reps']} - @{entry['rpe']}")