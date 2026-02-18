from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys
import process as pc

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
        self.signup.clicked.connect(self.create_account)

    def login_user(self):
        logged_in = pc.login(self.username.text())
        if not logged_in:
            self.error_label.setText("Invalid user")
        else:
            self.error_label.setText("valid user")
        self.error_label.show()

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

    def create_account(self):
        exists = pc.check_login(self.username.text())
        if not exists:
            pc.create_user(self.username.text())
            self.close()
        else:
            self.error_label.show()


main_window = LoginWindow()
main_window.show()
app.exec()
