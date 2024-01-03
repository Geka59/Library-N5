from unittest import TestCase, mock
from unittest.mock import patch
import pytest
from database import Database, DeletingError


class DatabaseTest(TestCase):

    @staticmethod
    def static_id_user(id):
        if id == None:
            return None
        return [["Василий", "Вячеславович"]]

    @mock.patch('database.sqlite3')
    @patch.object(Database, 'get_user_name_by_id', side_effect=static_id_user)
    def test_ret_user_name_on_id(self, sqlite3, db_mock):
        # sqlite3.connect.return_value.cursor.return_value.fetchall.return_value = [["a", "b"]]
        db = Database()
        self.assertEqual(db.ret_user_name_on_id(1), "Василий Вячеславович")
        self.assertRaises(TypeError, db.ret_user_name_on_id, None)

    @mock.patch('database.sqlite3')
    #@patch.object(Database)
    def test_check_id_in_base(self,sqlite3):
        sqlite3.connect.return_value.cursor.return_value.fetchall.return_value = [(2,), (3,)]
        db = Database()

        self.assertEqual(db.check_id_in_base([(2,), (3,)]), True)
        self.assertEqual(db.check_id_in_base([(1,), (6,)]), False)
        self.assertEqual(db.check_id_in_base([]), True)

    @mock.patch('database.sqlite3')
    def test_exec_book_name_on_id(self,sqlite3):
        sqlite3.connect.return_value.cursor.return_value.fetchone.return_value = ["Капитанский тест"]
        db = Database()
        assert db.exec_book_name_on_id(3) == "Капитанский тест"

    @mock.patch('database.sqlite3')
    @patch.object(Database,'ret_user_name_on_id', return_value='Евгений Сыпало')
    @patch.object(Database, 'check_id_in_base', return_value=True)
    def test_print_in_giu(self, chek, fovat, sqlite3):
        ###preparing data
        expected_result1=[['2', 'Как вывести октавию на сверхвук ', 'Б.Р. Штольц\n',
                          'dsgf', 'Евгений Сыпало', '24.09.2023', '25.09.2023']]

        expected_result2 = [['2', 'Как вывести октавию на сверхвук ', 'Б.Р. Штольц\n',
                             'dsgf', 'Выдано', '25.09.2023','']]
        first_data_res1 = [(2,)]
        second_data_res1 = [(2, 'Как вывести октавию на сверхвук ', 'dsgf', 1, '24.09.2023', '25.09.2023')]
        third_data_res1 = [('Б.Р. Штольц',)] # Возврат авторов

        ###finish preparing data
        sqlite3.connect.return_value.cursor.return_value.fetchall.side_effect = [first_data_res1 , second_data_res1, third_data_res1,second_data_res1,third_data_res1]
        db = Database()
        self.assertEqual(db.print_in_giu(None,1),expected_result1)
        self.assertEqual(db.print_in_giu([(2,)], 0),expected_result2)

    @mock.patch('database.sqlite3')
    @patch.object(Database,'adding_book')
    @patch.object(Database, 'ret_id_author')
    def test_check_adding(self,mock_id_author,moсk_adding_book,sqlite3):
        db = Database()
        moсk_adding_book.return_value=3 #возращаемый id
        mock_id_author.return_value=None
        #sqlite3.connect.return_value.cursor.return_value.fetchall.side_effect = [[('Книга1')],[],[('Автор1',)],[('Автор2',)],[('Автор3',)]]
        self.assertEqual(db.check_adding(['','','','',''],2),([1],[]))
        self.assertEqual(db.check_adding(['Book name', 'book desc', 'Author1', '', ''], 1), ([3,'Author1'],['Book name', 'book desc', 'Author1', '', ''],1))

        #self.assertEqual(db.check_adding('Book name', 'book desc', 'Author1', '', '', 1), 0)

    @mock.patch('database.sqlite3')
    def test_deletingt(self,sqlite3):
        sqlite3.connect.return_value.cursor.return_value.fetchall.return_value = [('1',)]
        db=Database()
        with pytest.raises(DeletingError):
            assert db.deletingt('3')==None
