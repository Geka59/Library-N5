from postgre_database import DatabasePostgre
from user_interface import UserInterface


def main():
    db = DatabasePostgre("postgres")
    # db.connect()
    ui = UserInterface(db)
    ui.ui_start()


if __name__ == "__main__":
    main()
