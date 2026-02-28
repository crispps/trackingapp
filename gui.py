from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QHBoxLayout, QComboBox, QMdiSubWindow, QMdiArea, QListWidget, QCheckBox
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys
import process as pc

app = QApplication([])


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting up window
        self.w = None  # Blank variable to set up sub window to create account
        self.setFixedSize(600, 400)
        self.setWindowTitle("trackingapp")

        # window.setWindowIcon(QIcon("icon.png"))

        self.Titletext = QLabel("Welcome to trackingapp", self)
        self.Titletext.setFixedHeight(50)
        self.username = QLineEdit()
        self.username.setFixedWidth(300)

        self.error_label = QLabel("gfdgd", self)
        self.error_label.move(300, 125)
        self.error_label.hide()

        self.username.setPlaceholderText("username:")
        self.login = QPushButton("Login")
        self.signup = QPushButton("Create\nAccount")
        self.login.setFixedSize(100, 50)
        self.signup.setFixedSize(100, 50)

        self.font = QFont()
        self.font.setPointSize(20)
        self.username.setFont(self.font)
        self.Titletext.setFont(self.font)
        self.font.setPointSize(12)
        self.login.setFont(self.font)
        self.signup.setFont(self.font)
        self.error_label.setFont(self.font)

        # Setting up layouts

        self.login_signup = QHBoxLayout()
        self.login_signup.addWidget(self.login)
        self.login_signup.addWidget(self.signup)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.Titletext)
        self.vertical_layout.addWidget(self.username)
        self.vertical_layout.addLayout(self.login_signup)

        self.widget = QWidget()
        self.widget.setLayout(self.vertical_layout)
        self.setCentralWidget(self.widget)

        # Setting up signals

        self.login.clicked.connect(self.login_user)
        self.signup.clicked.connect(self.create_account)

    def login_user(self):
        logged_in = pc.login(self.username.text())
        print(logged_in)
        if not logged_in:
            self.error_label.setText("Invalid user")
            self.error_label.show()
        else:
            self.w = MainWindow()
            self.w.show()
            self.close()

    def create_account(self, ):
        if self.w is None:
            self.w = CreateAccount()
        self.w.show()


class CreateAccount(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("create account")
        self.setFixedSize(300, 200)

        # creating widgets

        self.titletext = QLabel("Create Account", self)
        self.titletext.setFixedHeight(50)

        self.username = QLineEdit()
        self.username.setPlaceholderText("username:")

        self.create_button = QPushButton("Create")
        self.create_button.setFixedSize(100, 50)

        self.error_label = QLabel("Username already in use", self)
        self.error_label.setFixedWidth(200)
        self.error_label.move(75, 50)
        self.error_label.hide()

        # fonts

        self.font = QFont()
        self.font.setPointSize(20)
        self.titletext.setFont(self.font)
        self.username.setFont(self.font)
        self.create_button.setFont(self.font)

        # creating layouts

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.titletext)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.create_button)

        self.setLayout(self.layout)

        # signals

        self.create_button.clicked.connect(self.create_account)

    #   FIXED FOR DATABASE
    def create_account(self):
        exists = pc.check_username_exists(self.username.text())
        if not exists:
            pc.create_user(self.username.text())
            self.close()
        else:
            self.error_label.show()


class InputLift(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lifts = pc.user.get_lifts()
        self.error_label = QLabel()
        self.lift_selection = QComboBox()
        self.lift_selection.addItems(self.lifts)
        self.block = QComboBox()
        self.block.addItems(pc.get_blocks())
        self.date = QLineEdit()
        self.date.setPlaceholderText("date (YYYY-MM-DD):")
        self.weight = QLineEdit()
        self.weight.setPlaceholderText("weight:")
        self.sets = QLineEdit()
        self.sets.setPlaceholderText("sets:")
        self.reps = QLineEdit()
        self.reps.setPlaceholderText("reps:")
        self.rpe = QLineEdit()
        self.rpe.setPlaceholderText("rpe:")
        self.top_set = QCheckBox("Top set")
        self.submit = QPushButton("Submit")

        # layouts

        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(self.lift_selection)
        self.Hlayout.addWidget(self.error_label)
        self.Vlayout.addLayout(self.Hlayout)
        self.Vlayout.addWidget(self.block)
        self.Vlayout.addWidget(self.date)
        self.Vlayout.addWidget(self.weight)
        self.Vlayout.addWidget(self.sets)
        self.Vlayout.addWidget(self.reps)
        self.Vlayout.addWidget(self.rpe)
        self.Vlayout.addWidget(self.top_set)
        self.Vlayout.addWidget(self.submit)

        self.setLayout(self.Vlayout)

        # signals
        self.submit.clicked.connect(self.submit_data)

    def check_data(self, lift_data) -> str:
        error_message = ""
        # DATE CHECK
        if not pc.check_date_format(lift_data["date"]):
            error_message += "Invalid date format\n"
        if not pc.check_if_float(lift_data["weight"]):
            error_message += "Weight must be a number\n"
        if not pc.check_if_int(lift_data["sets"]):
            error_message += "Sets must be an integer\n"
        if not pc.check_if_int(lift_data["reps"]):
            error_message += "Reps must be an integer\n"
        if not pc.check_if_int(lift_data["rpe"]):
            error_message += "RPE must be an integer\n"
        return error_message

    def submit_data(self) -> None:
        error_message = ""
        lift_data = {
            "lift": self.lift_selection.currentText(),
            "block": self.block.currentText(),
            "date": self.date.text(),
            "weight": self.weight.text(),
            "sets": self.sets.text(),
            "reps": self.reps.text(),
            "rpe": self.rpe.text(),
            "top set": self.top_set.isChecked()
        }
        error_message = self.check_data(lift_data)
        if len(error_message) == 0:
            pc.submit_lift_data(lift_data)
        else:
            self.error_label.setText(error_message)


class ViewLifts(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # creating widgets

        self.lift_select = QComboBox()
        self.lift_select.addItems(pc.user.get_lifts())
        self.block_select = QComboBox()
        self.block_select.addItem("All blocks")
        self.block_select.addItems(pc.get_blocks())
        self.block_select.addItems(pc.user.get_blocks())
        self.lift_history = QListWidget()

        # layouts
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lift_select)
        self.layout.addWidget(self.block_select)
        self.layout.addWidget(self.lift_history)
        self.setLayout(self.layout)

        # signals

        self.lift_select.currentIndexChanged.connect(self.update_history)

    def update_history(self):
        lift_name = self.lift_select.currentText()
        history = pc.lift_history(lift_name)
        self.lift_history.clear()
        for entry in history:
            self.lift_history.addItem(f"{entry['date']} - {entry['weight']}kg - "
                                      f"{entry['sets']}x{entry['reps']} - @{entry['rpe']}")


class DataVisualisation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class NewLift(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # creating widgets

        self.error_label = QLabel()
        self.existing_lifts = QListWidget()
        self.existing_lifts.addItems(pc.user.get_lifts())
        self.enter_lift_text = QLabel("Enter lift name:")
        self.lift_name = QLineEdit()
        self.submit = QPushButton("Submit")

        # layouts

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.existing_lifts)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.enter_lift_text)
        self.layout.addWidget(self.lift_name)
        self.layout.addWidget(self.submit)
        self.setLayout(self.layout)

        # signals

        self.submit.clicked.connect(self.create_lift)

    def create_lift(self):
        lift_name = self.lift_name.text()
        if lift_name == "":
            self.error_label.setText("Enter lift name")
            return
        created = pc.new_lift(lift_name)
        if created:
            self.existing_lifts.addItem(lift_name)
        else:
            self.error_label.setText("Lift already exists")


class NewBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # creating widgets

        self.existing_blocks = QListWidget()
        self.existing_blocks.addItems(pc.get_blocks())
        self.block_type = QComboBox()
        self.block_type.addItems(["Training", "Peaking", "Deload", "Taper", "Comp"])
        self.name_label = QLabel("Block Name:")
        self.block_name = QLineEdit()
        self.submit = QPushButton("Submit")

        # layouts

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.existing_blocks)
        self.layout.addWidget(self.block_type)
        self.layout.addWidget(self.block_name)
        self.layout.addWidget(self.submit)
        self.setLayout(self.layout)

        # signals

        self.submit.clicked.connect(self.create_block)

    def create_block(self):
        created = pc.create_block(self.block_type.currentText(), self.block_name.text())
        if created:
            self.existing_blocks.addItem(self.block_name.text())
        else:
            self.name_label.setText("Block Name:     Block created")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting up window
        self.w = None  # Blank variable to set up sub window to create account
        self.setFixedSize(800, 500)
        self.setWindowTitle("trackingapp")

        # central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # creating widgets

        self.menu = QComboBox(self)
        self.menu_options = ["Home", "Input lift", "View lifts", "Data visualisation", "New lift", "New block"]
        self.menu.addItems(self.menu_options)
        self.display = QWidget()

        # layouts

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.display)

        self.setLayout(self.layout)

        # signals
        self.menu.currentIndexChanged.connect(self.menu_option)

    def menu_option(self):
        option = self.menu_options[self.menu.currentIndex()]

        # remove old widget
        old_widget = self.layout.itemAt(1).widget()
        self.layout.removeWidget(old_widget)
        old_widget.hide()
        if option == "Input lift":
            self.display = InputLift()
        elif option == "New lift":
            self.display = NewLift()
        elif option == "View lifts":
            self.display = ViewLifts()
        elif option == "New block":
            self.display = NewBlock()
        self.layout.addWidget(self.display)
        self.display.show()


def run_gui() -> None:
    main_window = LoginWindow()
    main_window.show()
    app.exec()
