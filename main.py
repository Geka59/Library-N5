from user_interface import UserInterface
from database import Database


def main():
    #db = Database()
    #db.connect()
    ui = UserInterface() #ui = UserInterface(db)
    ui.ui_start()


if __name__ == '__main__':
    main()
