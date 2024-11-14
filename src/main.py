from postgre_database import DatabasePostgre
from user_interface import UserInterface
from app import WebApp


def main():
    db = DatabasePostgre("postgres")
    # db.connect()
    web_app=WebApp()
    web_app.app_start()
    #ui = UserInterface(db)
    #ui.ui_start()


if __name__ == "__main__":
    main()
