

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
