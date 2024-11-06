import psycopg2
from database import Database #наследование класса бд

class DatabasePostgre(Database):
    def __init__(self,pg_db_name):
        self.db_library=psycopg2.connect(host="localhost",
            dbname=pg_db_name,user="postgres",password="1234",port=5432)
        self.cursor=self.db_library.cursor()
        # keif=2
        # self.cursor.execute("SELECT * FROM library5 WHERE id = %s",[keif])
        # self.cursor.execute("INSERT INTO books_authors VALUES(%s,%s)", [44, 44])
        # self.cursor.execute("INSERT INTO authors (author_name) VALUES(%s)", ['sdfdafdfs'])
        # self.db_library.commit()
        #print(self.cursor.fetchall())
# DatabasePostgre()