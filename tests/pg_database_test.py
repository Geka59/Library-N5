from unittest import TestCase, mock
import pytest
from postgre_database import DatabasePostgre
import psycopg2
class PgDatabaseTest(TestCase):
    pg_f_db=DatabasePostgre('test_pg')
    db_library = psycopg2.connect(host="localhost",
                                       dbname='test_pg', user="postgres", password="1234", port=5432)
    cursor_tb = db_library.cursor()  ### инициализация fake бд
    def adding_items_in_base_library5(self):
        #self.db_library = psycopg2.connect(host="localhost",
                                           #dbname='test_pg', user="postgres", password="1234", port=5432)
        #self.cursor_tb = self.db_library.cursor() ### инициализация fake бд

        self.cursor_tb.execute("DELETE FROM library5")
        self.db_library.commit()
        wr_data_test=[[1,'Название книги1','Описание книги1'],[2,'Название книги2','Описание книги2'],[3,'Название книги3','Описание книги3']]
        for i in range(0,len(wr_data_test)):
            self.cursor_tb.execute("INSERT INTO library5 (id,name,annotation) VALUES(%s,%s,%s)", wr_data_test[i])
        self.db_library.commit()

    def adding_items_authors(self):
        "Добавление 3 авторов для тсетирования"
        self.cursor_tb.execute("DELETE FROM authors")
        self.db_library.commit()
        wr_data_test = [[1, 'Ф.М. Достоевский'], [2, 'Л.Н. Толстой'],
                        [3, 'А.С. Пушкин']]
        for i in range(0, len(wr_data_test)):
            self.cursor_tb.execute("INSERT INTO authors (id,author_name) VALUES(%s,%s)", wr_data_test[i])
        self.db_library.commit()
#/////////////////////////////// Функиции подготовки данных для тестов

    def test_check_id_in_base(self):
        self.adding_items_in_base_library5()
        responce=self.pg_f_db.check_id_in_base([(1,), (2,), (3,),])
        assert responce==True
        responce1 = self.pg_f_db.check_id_in_base([(1,), (2,), (3,),(5,)])
        assert responce1 == False

    def test_exec_book_name_on_id(self):
        self.adding_items_in_base_library5()
        responce=self.pg_f_db.exec_book_name_on_id(3)
        assert responce=='Название книги3'
        responce = self.pg_f_db.exec_book_name_on_id(0)
        assert responce == None

    def test_print_in_giu(self):
        self.adding_items_in_base_library5()
        responce1=self.pg_f_db.print_in_giu([(1,)],1)
        assert responce1==[['1', 'Название книги1', '', 'Описание книги1', '', '', '']]
        responce2 = self.pg_f_db.print_in_giu([(0,)], 1)
        assert responce2 == []
        responce3 = self.pg_f_db.print_in_giu(None, 0)
        assert responce3 == [['1', 'Название книги1', '', 'Описание книги1', '', '', ''],['2', 'Название книги2', '', 'Описание книги2', '', '', ''],['3', 'Название книги3', '', 'Описание книги3', '', '', '']]


    def test_giving_book(self):
        self.adding_items_in_base_library5()
        self.pg_f_db.giving_book(2,2,'12.08.2024','12.08.2024')
        self.cursor_tb.execute("SELECT * From library5 WHERE id=2")
        resp_update=self.cursor_tb.fetchall()
        assert resp_update==[(2, 'Название книги2', 'Описание книги2', 2, '12.08.2024', '12.08.2024')]

    def test_users_on_name(self):
        self.adding_items_in_base_library5()

    def test_check_adding(self):
        self.adding_items_authors()
        responce=self.pg_f_db.check_adding(['Название книги', 'Описание книги', 'Н.М. Автор', '.. ', '.. '],1)
        assert responce==([3, 'Н.М. Автор'], ['Название книги', 'Описание книги', 'Н.М. Автор', '.. ', '.. '],1)
        responce = self.pg_f_db.check_adding(['Название книги1', 'Описание книги', 'Ф.М. Достоевский', '.. ', '.. '], 1)
        assert responce == ([2, 1], ['Название книги1', 'Описание книги', 'Ф.М. Достоевский', '.. ', '.. '], 1)

    def test_adding_book(self):
        self.adding_items_authors()
        self.pg_f_db.adding_writer()