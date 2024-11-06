# База данных хранящая сведения о всех книгах бибилиотеки №5 и читателях. БД состоит из 3 талбиц с
# 1 Таблица хранит книги с кодами авторов.
# 2 Таблица Данные о авторах
# 3 Таблица Данные о читателях и работиках библиотеки
# рефаткоринг database по отдельным функицям+ переписать тесты
# тесты на ui ask how highlite part code 36-2


# Поиск с фильтрацией
# динамические qCompliter
# поиск подстроки в комплитерах
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
        all_db = self.cursor.fetchall()
        # print(all_db)
        return all_db

    def check_id_in_base(self, data_check):
        """Проверка существовяния всех id списка data_check в базе"""
        id_for_check = data_check
        if len(id_for_check) == 0:
            return True
        all_id = self.cel_all_id_base()
        lice = [all_id[i][0] for i in range(0, len(all_id))]
        for i in range(0, len(id_for_check)):
            if ((id_for_check)[i][0] not in lice):
                return False
        return True

    def cel_all_id_base(self):
        self.cursor.execute("SELECT id FROM library5")
        return self.cursor.fetchall()

    def login_user(self, user_name, password):
        self.cursor.execute("SELECT * FROM users WHERE login = %s", [user_name])
        user_data = self.cursor.fetchall()
        return user_data

    def exec_book_name_on_id(self, id_book):
        '''Возвращает название книги по ее id'''
        self.cursor.execute("SELECT name FROM library5 WHERE id = %s", [id_book])
        book_name = self.cursor.fetchone()
        if book_name!=None:
            return book_name[0]
        else:
            return None

    def cel_lib5_on_id(self, i):
        self.cursor.execute("SELECT * FROM library5 WHERE id=%s", [i])
        return (self.cursor.fetchall())

    def cel_different_data(self, i):
        self.cursor.execute(  # authors.id
            "SELECT authors.author_name FROM authors LEFT OUTER JOIN books_authors ON authors.id = "
            "books_authors.author_id WHERE books_authors.book_id = %s", [i])
        return (self.cursor.fetchall())

    def print_in_giu(self, id, id_swich):
        """Выборка данных из таблиц library5 и authors для вывода
        id_swich 0- отображает Выдано или нет
        id_swich 1- отображает имя кому выдано и когда
        """
        if id is None:
            selection = self.cel_all_id_base()
        else:
            if (self.check_id_in_base(id)) == False:
                return []
            selection = id
        list_out = [''] * len(selection)  # спиоск собирающийся на вывод
        k: int
        for k in range(len(selection)):
            list_out[k] = [''] * 7
        bounty = 0
        for ik in selection:
            i = ik[0]
            var1 = self.cel_lib5_on_id(i)

            var2 = self.cel_different_data(i)

            list_out[bounty][0] = str(var1[0][0])  # bug
            list_out[bounty][1] = str(var1[0][1])
            var3 = ''
            for h in range(0, (len(var2))):
                var3 = var3 + str(var2[h][0]) + "\n"
            list_out[bounty][2] = var3
            list_out[bounty][3] = str(var1[0][2])

            if (str(var1[0][3])) != 'None':
                list_out[bounty][5] = str(var1[0][5])
                if id_swich == 1:
                    name = self.ret_user_name_on_id(str(var1[0][3]))
                    list_out[bounty][4] = name
                    list_out[bounty][5] = str(var1[0][4])
                    list_out[bounty][6] = str(var1[0][5])
                else:
                    list_out[bounty][4] = 'Выдано'
                if id_swich == 2:
                    list_out[bounty][4] = str(var1[0][4])

            bounty += 1
        vivod = list_out
        return vivod

    def giving_book(self, id_user, id_book, date_now, date_ret):
        self.cursor.execute("UPDATE library5 SET reader=%s, date_given_out=%s, date_return=%s WHERE id=%s",
                            [id_user, date_now, date_ret, id_book])
        self.db_library.commit()

    def return_book_bd(self, id_book):
        self.cursor.execute("UPDATE library5 SET reader=%s, date_given_out=%s, date_return=%s WHERE id=%s",
                            [None, None, None, id_book])
        self.db_library.commit()

    def get_user_name_by_id(self, id):
        self.cursor.execute("SELECT name,surname from users WHERE id=%s", [id])
        return self.cursor.fetchall()

    def get_name_surname_all(self):
        self.cursor.execute("SELECT name,surname FROM users")
        return self.cursor.fetchall()

    def get_authors_name(self):
        self.cursor.execute("SELECT author_name FROM authors")
        return self.cursor.fetchall()

    def get_books_names(self):
        self.cursor.execute("SELECT name FROM library5")
        return self.cursor.fetchall()

    def ret_user_name_on_id(self, id):
        user_data = self.get_user_name_by_id(id)
        reverse_user_data = user_data[0][0] + ' ' + user_data[0][1]
        return reverse_user_data

    def users_on_name(self, all_name):
        parse = all_name.find(' ')
        if parse != -1:
            name = all_name[:parse]
            surname = all_name[parse + 1:]
            search_in_table = '%' + name + '%'
            search_in_sur = '%' + surname + '%'
            self.cursor.execute(
                "SELECT * FROM users WHERE name LIKE %s AND surname LIKE %s OR name LIKE %s AND surname LIKE %s",
                [search_in_table, search_in_sur, search_in_sur, search_in_table])
            return (self.cursor.fetchall())
        else:
            search_name = '%' + all_name + '%'
            self.cursor.execute("SELECT * FROM users WHERE name LIKE %s OR surname LIKE %s", [search_name, search_name])
            return self.cursor.fetchall()

    def book_on_id_user(self, id_user):
        """Возвращает ввсе id книг которые читаются пользователем с id"""
        self.cursor.execute("SELECT id from library5 WHERE reader=%s", [id_user])
        return self.cursor.fetchall()

    def check_adding(self, data_about_book, count_authors):
        '''Прооверка введеных данных на добавление книги'''
        if (data_about_book[0] == '' or data_about_book[1] == ''):
            return [1], []
        for m in range(count_authors):
            if len(data_about_book[2 + m]) < 4:
                return [1], []  # Проверка на пустые поля

        book_name = data_about_book[0]
        for i in range(count_authors):
            id_author = self.ret_id_author(data_about_book[i + 2])  # выбор авторов из массива
            if id_author is None:
                print(f'{i + 1} Автора нет')
                return [3, data_about_book[i + 2]], data_about_book, count_authors
        ###Проверка существования данной книги
        book_in_base = self.ret_id_book(data_about_book[0])
        if book_in_base != []:
            for k in range(len(book_in_base)):
                print(f'Такая книжка уже есть с id{book_in_base[k][0]}')
                return [2, book_in_base[k][0]], data_about_book, count_authors
        # чето делаем
        # выводим ошибки если еть retur
        id_book = self.adding_book(data_about_book, count_authors)  # Все ок можно добавлять
        return [0], [id_book]

    def ret_id_book(self, name_book):
        self.cursor.execute("SELECT id FROM library5 WHERE name=%s", [name_book])
        return self.cursor.fetchall()

    def ret_id_author(self, author_name):
        self.cursor.execute("SELECT id FROM authors WHERE author_name=%s", [author_name])
        return self.cursor.fetchone()

    def cel_add_book(self, wr_data):
        self.cursor.execute("INSERT INTO library5 (name,annotation) VALUES(%s,%s)", wr_data)
        self.db_library.commit()

    def cel_add_communication(self, book_id, author_id):
        self.cursor.execute("INSERT INTO books_authors VALUES(%s,%s)", [book_id, author_id])

    def adding_book(self, book_data, count_authors):
        print(book_data)
        wbook_name = book_data[0]
        wbook_descript = book_data[1]
        wr_data = [wbook_name, wbook_descript]
        self.cel_add_book(wr_data)
        book_id = max(self.ret_id_book(book_data[0]))[0]
        print(book_id)
        for i in range(count_authors):
            author_id = self.ret_id_author(book_data[2 + i])[0]
            self.cel_add_communication(book_id, author_id)
        self.db_library.commit()
        return book_id
        # Надо написать все океее

    def adding_writer(self, author):  # Отправки запроса на кнопку добавления автора
        # wr_data_a = [None, author]
        wr_data_a = [str(author)]
        self.cursor.execute("INSERT INTO authors (author_name) VALUES(%s)", wr_data_a)
        self.db_library.commit()

    def cel_deleting_from_library5(self, id_book):
        self.cursor.execute("DELETE FROM library5 WHERE id=%s", [id_book])

    def cel_deleting_from_books_authors(self, id_book):
        self.cursor.execute("DELETE FROM books_authors WHERE book_id=%s", [id_book])

    def deletingt(self, id_book):
        list_for_check = []
        id_list = self.cel_all_id_base()
        for num in range(0, len(id_list)):
            list_for_check.append(id_list[num][0])
        if (id_book in list_for_check):
            self.cel_deleting_from_library5(id_book)
            self.cel_deleting_from_books_authors(id_book)
            self.db_library.commit()
        else:
            print('Ошибка индекса')
            raise DeletingError

    def authors_looking_as(self, name):
        ready_name = '%' + name + '%'
        self.cursor.execute("SELECT author_name FROM authors WHERE author_name LIKE %s", ['пушкин'])
        return self.cursor.fetchall()

    def search_fetchall(self, search_text, search_bool):
        """"
        Выбор id книг для вывода для пользователя
        search_text - тескт прилетевший с поля ввода
        seaech_bool - массив [bool_authors,bool_books,bool_desc,bool_given]
        """
        # if search_bool == 1:  # поиск по названию книги возвращает спиок id
        #     search_in_table = '%' + search_text + '%'
        #     self.cursor.execute("SELECT id FROM library5 WHERE name LIKE %s", [search_in_table])
        #     # print(self.cursor.fetchall())
        #     return (self.cursor.fetchall())
        # arr_request=[ "SELECT library5.id FROM authors "
        #             "INNER JOIN books_authors ON authors.id = books_authors.author_id "
        #             "INNER JOIN library5 ON library5.id = books_authors.book_id " # todo объединяем несколько sql запросов
        #             f"WHERE author_name LIKE %s","SELECT id FROM library5 WHERE name LIKE %s","SELECT id FROM "
        #             f"library5 WHERE annotation LIKE %s",]
        # arr_sqlite=[]
        #
        # for i in range(len(search_bool[:3])):
        #     if search_bool[i]==True: # todo переделать на sum
        #         arr_sqlite.append(search_in_table)
        # #начинаем колхоз создаем массив данных на поиск
        # request="SELECT library5.id FROM authors INNER JOIN books_authors ON authors.id = books_authors.author_id " \
        #         "INNER JOIN library5 ON library5.id = books_authors.book_id WHERE author_name LIKE %s "*search_bool[0] \
        #         + " SELECT id FROM library5 WHERE name LIKE %s "*search_bool[1]+" SELECT id FROM library5 WHERE " \
        #                                                                      "annotation LIKE %s "*search_bool[
        #             2]+"INTERSECT "*search_bool[3]*bool(sum(search_bool[:3]))+"SELECT id FROM library5 WHERE reader IS NOT NULL"*search_bool[3]
        # # ... WHERE ( %s=True and Name like %s ) " , [ isFilterByName, text ]
        # print(search_bool)
        # request_with_union=" UNION ".join(request.split('  '))
        # print(request_with_union)
        # self.cursor.execute(request_with_union,arr_sqlite)
        if search_text == '':
            return None
        search_in_table = '%' + search_text + '%'  # todo объединяем несколько sql запросов
        self.cursor.execute("SELECT library5.id "
                            "FROM library5 "
                            "LEFT JOIN books_authors ON library5.id = books_authors.book_id "
                            "LEFT JOIN authors ON authors.id = books_authors.author_id "
                            "WHERE ("
                            "        (%s and author_name LIKE %s) "
                            "        OR (%s and name LIKE %s) "
                            "        OR (%s and annotation LIKE %s)"
                            "    )  AND (NOT %s OR library5.reader IS NOT NULL)",
                            [search_bool[0], search_in_table, search_bool[1],
                             search_in_table, search_bool[2], search_in_table, search_bool[3]])
        output = self.cursor.fetchall()
        print(output)
        # self.cursor.execute(
        #             "SELECT library5.id FROM authors "
        #             "INNER JOIN books_authors ON authors.id = books_authors.author_id "
        #             "INNER JOIN library5 ON library5.id = books_authors.book_id " #
        #             f"WHERE author_name LIKE %s UNION SELECT id FROM library5 WHERE name LIKE %s UNION SELECT id FROM "
        #             f"library5 WHERE annotation LIKE %s", [search_in_table,search_in_table,search_in_table])
        return output

        ### ищем по описанию книги
        # search_in_table = '%' + search_text + '%'
        # self.cursor.execute("SELECT id FROM library5 WHERE annotation LIKE %s", [search_in_table])
        # #return (self.cursor.fetchall())
