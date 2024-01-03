from unittest import TestCase, mock
from unittest.mock import patch
import pytest
from database import Database

from user_interface import UserInterface


class UITest(TestCase):
    @mock.patch('user_interface.uic')
    @patch.object(UserInterface, 'setColortoRow')
    def test_out_table(self, mock_color_row, mock_uic):
        tui = UserInterface()
        tui.out_table(
            [['2', 'Как вывести октавию на сверхвук ', 'Б.Р. Штольц\n', 'gdf', 'Евгк', '24.09.2023', '25.09.2023']])
        mock_color_row.assert_called_with(0, 1)
        mock_data = tui.ui.tableWidget.setItem.call_count
        assert mock_data == 14

    @mock.patch('user_interface.QMessageBox')
    def test_print_succes(self, mock_qt):
        ui = UserInterface()
        ui.print_succes('test_message_text')
        self.assertEqual(mock_qt.call_count, 3)

    @mock.patch('user_interface.uic', autospec=True)
    def test_setColorRow(self, mock_bb):
        tui = UserInterface()
        tui.setColortoRow(2, 0)
        tui.ui.tableWidget_2.item.assert_called_once()
        tui.setColortoRow(2, 1)
        tui.aui.tableWidget.item.assert_called_once()
        tui.setColortoRow(2, 2)
        self.assertEqual(tui.aui.tableWidget_2.item.call_args.args, (2, 0))

    @patch.object(UserInterface, 'setColortoRow')
    @patch.object(UserInterface, 'data_revision')
    def test_admin_out_table_my_books(self, mock_datarev, mocking_def):
        tui = UserInterface()
        tui.admin_out_table_my_books(
            [['2', 'Как вывести октавию на сверхвук ', 'Б.Р. Штольц\n', 'gdf', '24.09.2023', '25.09.2023']])
        mocking_def.assert_called_with(0, 2)
        mock_datarev.assert_called_with('25.09.2023')

    @mock.patch('user_interface.uic')
    def test_out_table_my_books(self, mockd):
        tui = UserInterface()
        tui.out_table_my_books(
            [['2', 'Как вывести октавию на сверхвук ', 'Б.Р. Штольц\n', 'gdf', '24.09.2023', '25.09.2023']])
        mock_data = tui.ui.tableWidget_2.setRowCount.call_args.args
        assert mock_data == (1,)

    def test_data_revision(self):
        tui = UserInterface()
        self.assertEqual(tui.data_revision('25.09.2050'), None)
        self.assertEqual(tui.data_revision('25.09.2010'), True)

    @patch.object(Database, 'login_user')
    def test_login_user(self, mock_db):
        mock_db.return_value = [(3, 'fsoky', '1234', 'Петр', 'Ник', 0, None)]
        tui = UserInterface()
        tui.login_user()
        mock_db.assert_not_called()

    @mock.patch('user_interface.uic')
    @patch.object(Database, 'users_on_name')
    @patch.object(Database, 'print_in_giu')
    @patch.object(Database, 'book_on_id_user')
    def test_search_id(self, mock_book_on_id, mock_print_gui, mock_users_id, mock_ui):
        mock_print_gui.return_value = [(3, 'Name book', 'Author', 'Desc', '12.09.2023', '23.04.2024')]
        mock_book_on_id.return_value = [3, 4]
        mock_users_id.return_value = [(3, 'Name', 'Surname', 'role')]
        tui = UserInterface()
        tui.search_id()
        mock_data = tui.aui.lineEdit_13.setText.call_args.args
        assert mock_data == ('3',)
        mock_users_id.return_value = []
        tui.search_id()
        mock_data = tui.aui.lineEdit_13.setText.call_args.args
        assert mock_data == ('',)

    @patch.object(Database, 'book_on_id_user')
    @patch.object(Database, 'print_in_giu')
    @mock.patch('user_interface.uic')
    def test_enterance(self, mocked_ui, mock_db_print, mock_book_on_id):
        tui = UserInterface()
        tui.enterance('User_name', '3')
        mock_db_print.return_value = [('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        mock_book_on_id.return_value = [(1,)]
        mock_data = tui.ui.label_6.setText.call_args.args
        assert mock_data == ('User_name',)

    @patch.object(Database, 'print_in_giu')
    @mock.patch('user_interface.uic')
    def test_admin_enterance(self, mocked_ui, mock_db_print, ):
        tui = UserInterface()
        tui.admin_enterance()
        mock_db_print.return_value = [('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        tui.aui.show.assert_called_once()

    @mock.patch('user_interface.uic')
    def test_index_changed(self, mocked_ui):
        tui = UserInterface()
        tui.index_changed()
        tui.aui.lineEdit_4.hide.assert_called()

    @mock.patch('user_interface.uic')
    def test_visible_button(self, mocked_ui):
        tui = UserInterface()
        tui.visible_butt(1)
        tui.aui.pushButton_2.show.assert_called()

    @patch.object(UserInterface, 'out_table')
    @patch.object(Database, 'print_in_giu')
    @patch.object(Database, 'check_adding')
    @patch.object(UserInterface, 'info')
    # @mock.patch('user_interface.uic')
    def test_check_data_adding_book(self, info_mcok, mock_check, mock_db_print, mock_fun_ui):
        tui = UserInterface()
        mock_check.return_value = [0], [4]
        mock_db_print.return_value = [('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        tui.check_data_adding_book()
        mock_fun_ui.assert_called()

    @patch.object(UserInterface, 'print_succes')
    @mock.patch('user_interface.uic')
    def test_info(self, mocked_ui, mock_print):
        tui = UserInterface()
        tui.info([[0], [1]])
        mock_print.assert_called_with(f'✅   Книга добавлена id {1}')

    @patch.object(Database, 'adding_book')
    @patch.object(Database, 'adding_writer')
    @patch.object(UserInterface, 'print_succes')
    def test_dialog_result(self, mock_print_succes, mock_adding_writer, mock_adding_book):
        tui = UserInterface()
        mock_adding_writer.return_value = 55
        mock_adding_book.return_value = 55
        tui.dialog_result(1024, [[3, 55], [1]])
        mock_print_succes.assert_called_with(f'✅       Автор {55} добавлен')

        tui.dialog_result(1024, [[2, 55], [1], [0]])
        mock_print_succes.assert_called_with(f'✅   Книга добавлена id {55}')

    @patch.object(UserInterface, 'admin_out_table_my_books')
    @patch.object(Database, 'giving_book')
    @patch.object(Database, 'book_on_id_user')
    @patch.object(Database, 'print_in_giu')
    @mock.patch('user_interface.uic')
    def test_given_out(self, mock_ui, mock_print_in_gui, mock_book_on_id_user, mock_giving_book, mock_admin_out):
        tui = UserInterface()
        mock_print_in_gui.return_value = [
            ('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        mock_book_on_id_user.return_value = [(2,)]
        mock_print_in_gui.return_value = [
            ('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        tui.given_out()
        mock_admin_out.assert_called_with(
            [('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')])

    @patch.object(UserInterface, 'admin_out_table_my_books')
    @patch.object(Database, 'return_book_bd')
    @patch.object(Database, 'book_on_id_user')
    @patch.object(Database, 'print_in_giu')
    @mock.patch('user_interface.uic')
    def test_return_book(self, mock_ui, mock_print_in_gui, mock_book_on_id_user, mock_return_book, mock_admin_out):
        tui = UserInterface()
        mock_print_in_gui.return_value = [
            ('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        mock_book_on_id_user.return_value = [(2,)]
        mock_print_in_gui.return_value = [
            ('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')]
        tui.return_book()
        mock_admin_out.assert_called_with(
            [('5', 'Капитанская дочка', 'А.С. Пушкин\n', 'Ном', 'Выдано', '29.08.2023', '')])
