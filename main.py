import process as pc
import tui


logged_in = False
choice = tui.start_menu()
if choice == "2":
    pc.create_user()
while not logged_in:
    logged_in = pc.login()
exit = False
while not exit:
    choice = tui.main_menu()
    if choice == "1":
        pc.submit_lift_data()
    elif choice == "2":
        pc.lift_history()
    elif choice == "3":
        pc.create_lift()

