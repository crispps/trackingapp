from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from user import User
import sys

app = QApplication([])


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting up window
        self.w = None   # Blank variable to set up sub window to create account
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

    def check_login(self) -> bool:
        import json
        with open("data/users.json", "r") as f:
            users = json.load(f)
        for i in users:
            if self.username.text() == i:
                return True
        return False

    def login_user(self):
        logged_in = False
        username = self.username.text()
        logged_in = self.check_login()
        if not logged_in:
            self.error_label.setText("Invalid user")
        else:
            self.error_label.setText("valid user")
        self.error_label.show()



class CreateAccount(QWidget):
    def __init__(self):
        super().__init__()


main_window = LoginWindow()
main_window.show()
app.exec()
