# База данных хранящая сведения о всех книгах бибилиотеки №5 и читателях. БД состоит из 3 талбиц с
# 1 Таблица хранит книги с кодами авторов.
# 2 Таблица Данные о авторах
# 3 Таблица Данные о читателях и работиках библиотеки
# рефаткоринг database по отдельным функицям+ переписать тесты
# тесты на ui ask how highlite part code
import sqlite3


# from sqlite3 import Cursor
class DeletingError(Exception):
    pass


class Database():

    def __init__(self):
        self.dbLib = sqlite3.connect("test_autors")
        self.cursor = self.dbLib.cursor()

    def print_all_db(self):
        print(self)
        self.cursor.execute("SELECT * FROM library5")
        all_db=self.cursor.fetchall()
        #print(all_db)
        return all_db

    def check_id_in_base(self,data_check):
        """Проверка существовяния всех id списка data_check в базе"""
        id_for_check=data_check
        if len(id_for_check)==0:
            return True
        self.cursor.execute("SELECT id FROM library5")
        all_id=self.cursor.fetchall()
        lice = [all_id[i][0] for i in range(0, len(all_id))]
        for i in range(0,len(id_for_check)):
            if((id_for_check)[i][0] not in lice):
                return False
        return True

    def login_user(self,user_name,password):
        self.cursor.execute("SELECT * FROM users WHERE login = ?", [user_name])
        user_data=self.cursor.fetchall()
        return user_data
    def exec_book_name_on_id(self, id_book):
        '''Возвращает название книги по ее id'''
        self.cursor.execute("SELECT name FROM library5 WHERE id = ?", [id_book])
        book_name = self.cursor.fetchone()
        print(book_name[0])
        return book_name[0]

    def print_in_giu(self, id, id_swich):
        """Выборка данных из таблиц library5 и authors для вывода"""
        if id is None:
            self.cursor.execute("SELECT id FROM library5")
            selection = self.cursor.fetchall()
        else:
            if (self.check_id_in_base(id))==False:
                return []
            selection = id
        list_out = [''] * len(selection)  # спиоск собирающийся на вывод
        k: int
        for k in range(len(selection)):
            list_out[k] = [''] * 7
        bounty = 0
        for ik in selection:
            i = ik[0]
            self.cursor.execute("SELECT * FROM library5 WHERE id=?", [i])
            var1 = list(self.cursor.fetchall())
            self.cursor.execute(  # authors.id
                "SELECT authors.author_name FROM authors LEFT OUTER JOIN books_authors ON authors.id = "
                "books_authors.author_id WHERE books_authors.book_id = ?", [i])
            var2 = list(self.cursor.fetchall())

            list_out[bounty][0] = str(var1[0][0])  # bug
            list_out[bounty][1] = str(var1[0][1])
            var3 = ''
            for h in range(0, (len(var2))):
                var3 = var3 + str(var2[h][0]) + "\n"
            list_out[bounty][2] = var3
            list_out[bounty][3] = str(var1[0][2])

            if (str(var1[0][3]))!='None':
                list_out[bounty][5] = str(var1[0][5])
                if id_swich==1:
                    name=self.ret_user_name_on_id(str(var1[0][3]))
                    list_out[bounty][4] = name
                    list_out[bounty][5] = str(var1[0][4])
                    list_out[bounty][6] = str(var1[0][5])
                else:
                    list_out[bounty][4] = 'Выдано'
                if id_swich==2:
                    list_out[bounty][4] = str(var1[0][4])

            bounty += 1
        vivod = list_out

        # cursor.execute(
        # "SELECT Library5.id,Library5.name,autorsBook.author,Library5.annotation FROM Library5 "
        # "LEFT OUTER JOIN autorsBook WHERE autorsBook.id == (Library5.id_author)")

        return vivod

    def giving_book(self,id_user,id_book,date_now,date_ret):
        self.cursor.execute("UPDATE library5 SET reader=?, date_given_out=?, date_return=? WHERE id=?",[id_user,date_now,date_ret,id_book])
        self.dbLib.commit()

    def return_book_bd(self,id_book):
        self.cursor.execute("UPDATE library5 SET reader=?, date_given_out=?, date_return=? WHERE id=?",
                            [None, None, None, id_book])
        self.dbLib.commit()

    def get_user_name_by_id(self, id):
        self.cursor.execute("SELECT name,surname from users WHERE id=?", [id])
        return self.cursor.fetchall()

    def ret_user_name_on_id(self, id):
         user_data=self.get_user_name_by_id(id)
         reverse_user_data= user_data[0][0]+' '+user_data[0][1]
         return reverse_user_data

    def users_on_name(self,name,surname):
        search_in_table = '%' + name + '%'
        search_in_sur = '%' + surname + '%'
        self.cursor.execute("SELECT * FROM users WHERE name LIKE ? AND surname LIKE ?", [search_in_table,search_in_sur])
        return (self.cursor.fetchall())

    def book_on_id_user(self, id_user):
        """Возвращает ввсе id книг которые читаются пользователем с id"""
        self.cursor.execute("SELECT id from library5 WHERE reader=?",[id_user])
        return self.cursor.fetchall()

    def check_adding(self, book_name: str, book_descript: str, writer_book1: str, writer_book2: str, writer_book3: str,
                     count_authors: int):
        if ((len(book_name) == 0 or len(book_descript) == 0 or len(writer_book1) < 4) or (
                count_authors > 1 and len(writer_book2) < 4)):
            return 1
        self.cursor.execute("SELECT id FROM library5 WHERE name = ?", [book_name])
        if len(self.cursor.fetchall()) != 0:
            return 2
        self.cursor.execute("SELECT id FROM authors WHERE author_name=?", [writer_book1])
        aut1 = self.cursor.fetchone()
        self.cursor.execute("SELECT id FROM authors WHERE author_name=?", [writer_book2])
        aut2 = self.cursor.fetchone()
        self.cursor.execute("SELECT id FROM authors WHERE author_name=?", [writer_book3])
        aut3 = self.cursor.fetchone()

        if count_authors == 1:
            if aut1 is not None:

                self.adding_book(book_name, book_descript, aut1, aut2, aut3, count_authors)

            else:
                return 3
        elif count_authors == 2:
            if (aut1 is not None) and (aut2 is not None):
                self.adding_book(book_name, book_descript, aut1, aut2, aut3, count_authors)
            else:
                return 3
        elif count_authors == 3:
            if (aut1 is not None) and (aut2 is not None) and (aut3 is not None):
                self.adding_book(book_name, book_descript, aut1, aut2, aut3, count_authors)
            else:
                return 3

        return 0

    def adding_book(self, wbook_name, wbook_descript, author1_id, author2_id, author3_id, count_authors):
        wr_data = [None, wbook_name, wbook_descript, None]
        # raise CustomException
        # print('dffnfj')
        self.cursor.execute("INSERT INTO library5 VALUES(?,?,?,?)", wr_data)
        self.dbLib.commit()
        self.cursor.execute("SELECT id FROM library5 WHERE name=?", [wbook_name])
        book_id = self.cursor.fetchone()[0]
        self.cursor.execute("INSERT INTO books_authors VALUES(?,?)", [book_id, author1_id[0]])
        if count_authors == 2:
            self.cursor.execute("INSERT INTO books_authors VALUES(?,?)", [book_id, author2_id[0]])
        if count_authors == 3:
            self.cursor.execute("INSERT INTO books_authors VALUES(?,?)", [book_id, author3_id[0]])
        self.dbLib.commit()
        return None

    # #def adding_writer(self,author1, author2, author3, count_authors):  # Отправки запроса на кнопку добавления автора
    #   #  wr_data_a = [None, author1]
    #     cursor.execute("INSERT INTO authors VALUES(?,?)", wr_data_a)
    #     dbLib.commit
    def deletingt(self, id_book):
        list_for_check = []
        self.cursor.execute("SELECT id FROM library5")
        id_list = self.cursor.fetchall()
        for num in range(0, len(id_list)):
            list_for_check.append(id_list[num][0])
        if (id_book in list_for_check):
            self.cursor.execute("DELETE FROM library5 WHERE id=?", [id_book])
            self.cursor.execute("DELETE FROM books_authors WHERE book_id=?", [id_book])
            self.dbLib.commit()
        else:
            print('Ошибка индекса')
            raise DeletingError

    def search_fetchall(self, search_text, search_bool):
        """"Выбор id книг для вывода"""
        if search_bool == 1:  # поиск по названию книги возвращает спиок id
            search_in_table = '%' + search_text + '%'
            self.cursor.execute("SELECT id FROM library5 WHERE name LIKE ?", [search_in_table])
            # print(self.cursor.fetchall())
            return (self.cursor.fetchall())

        if search_bool == 0:  # поиск по автору
            if search_text == '':
                return None
            search_in_table = '%' + search_text + '%'
            self.cursor.execute(
                    "SELECT library5.id FROM authors "
                    "INNER JOIN books_authors ON authors.id = books_authors.author_id "
                    "INNER JOIN library5 ON library5.id = books_authors.book_id "
                    f"WHERE author_name LIKE ? ", [search_in_table])
            return self.cursor.fetchall()