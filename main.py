import process as pc
import tui

logged_in = False
choice = tui.main_menu()
if choice == "2":
    pc.create_user()
while not logged_in:
    logged_in = pc.login()


