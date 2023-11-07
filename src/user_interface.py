import pathlib

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QCompleter, QMessageBox
from database import Database
from datetime import datetime

ASSET_PATH = f"{pathlib.Path(__file__).parents[1]}/assets"
print(ASSET_PATH)


class UserInterface:
    app = None
    aui = None
    ui = None
    welcome_window = None
    bd = None

    def __init__(self):
        # init
        app = QtWidgets.QApplication([])
        welcome_window = uic.loadUi(f"{ASSET_PATH}\WelcomeWindow.ui")
        welcome_window.setWindowTitle(f"{ASSET_PATH}\Вход")
        aui: object = uic.loadUi(f"{ASSET_PATH}\AdminWindow.ui")
        ui = uic.loadUi(f"{ASSET_PATH}\WindowMain.ui")
        ui.setWindowTitle("Library № 5")  # Начальные настройки фронта
        aui.pushButton_2.hide()
        aui.comboBox.addItems(['1', '2', '3'])
        ui.comboBox.addItems(['Авторы', 'Книги'])
        aui.comboBox_3.addItems(['Авторы', 'Название'])
        aui.lineEdit_4.hide()
        aui.lineEdit_5.hide()
        self.err1 = QMessageBox()
        self.err1.setWindowTitle('Ошибка ввода')
        self.err1.setText('Некоторые поля не заполнены или не выбрана книга')
        self.err1.setIcon(QMessageBox.Warning)

        self.add_b = QMessageBox()
        self.add_b.setWindowTitle('Информация добавления книги')
        self.add_b.setText('Бип боп')
        self.add_b.setIcon(QMessageBox.Information)
        print("UI Init complited")
        self.app = app
        self.ui = ui
        self.aui = aui
        self.welcome_window = welcome_window
        self.bd = Database()

    def out_table(self, rows):  # Функция вывода датнных в таблицу пользовательского интерфейса
        print(f"out_table")
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setSortingEnabled(False)
        self.ui.tableWidget.setHorizontalHeaderLabels(['id книги', 'Название', 'Автор', 'Краткое описание', 'Выдано'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.ui.tableWidget.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.setSortingEnabled(True)

        """вывод в окно админа"""
        self.aui.tableWidget.setRowCount(len(rows))
        self.aui.tableWidget.setColumnCount(7)
        self.aui.tableWidget.setHorizontalHeaderLabels(
            ['id книги', 'Название', 'Автор', 'Краткое описание', 'Читатель', 'Дата выдачи', 'Дата возврата'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.aui.tableWidget.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
                if y == 6 and str(rows[x][y]) != '' and self.data_revision(str(rows[x][y])):
                    self.setColortoRow(x, 1)
        self.aui.tableWidget.resizeColumnsToContents()

    def out_table_my_books(self, rows):
        """вывод в окно моих книг"""
        self.ui.tableWidget_2.setRowCount(len(rows))
        self.ui.tableWidget_2.setColumnCount(6)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(
            ['id книги', 'Название', 'Автор', 'Краткое описание', 'дата выдачи', 'дата возврата'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.ui.tableWidget_2.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
                if y == 5 and self.data_revision(str(rows[x][y])):
                    self.setColortoRow(x, 0)
        self.ui.tableWidget_2.resizeColumnsToContents()

    def admin_out_table_my_books(self, rows):
        """вывод в окно книг человека"""
        self.aui.tableWidget_2.setRowCount(len(rows))
        self.aui.tableWidget_2.setColumnCount(6)
        self.aui.tableWidget_2.setHorizontalHeaderLabels(
            ['id книги', 'Название', 'Автор', 'Краткое описание', 'дата выдачи', 'дата возврата'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.aui.tableWidget_2.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
                if y == 5 and self.data_revision(str(rows[x][y])):
                    self.setColortoRow(x, 2)
        self.aui.tableWidget_2.resizeColumnsToContents()

    def print_succes(self,message_text):
        self.suc = QMessageBox()
        self.suc.setWindowTitle('Ура')
        self.suc.setText(message_text)
        #self.suc.setIcon(QMessageBox.Information)
        self.suc.exec()
    def data_revision(self, date_for_revision):
        current_date = datetime.now().date()
        current_date_string = current_date.strftime('%d.%m.%Y')
        # print(current_date_string)
        a = (datetime.strptime(date_for_revision, '%d.%m.%Y')).date()
        if (current_date > a):
            return True

    def setColortoRow(self, rowIndex, flag):
        '''Закраска таблиц по row index '''
        if flag == 0:
            for j in range(self.ui.tableWidget_2.columnCount()):
                self.ui.tableWidget_2.item(rowIndex, j).setBackground(QtGui.QColor(255, 125, 12))
        elif flag == 1:
            for j in range(self.aui.tableWidget.columnCount()):
                self.aui.tableWidget.item(rowIndex, j).setBackground(QtGui.QColor(255, 125, 12))
        else:
            for j in range(self.aui.tableWidget_2.columnCount()):
                self.aui.tableWidget_2.item(rowIndex, j).setBackground(QtGui.QColor(255, 125, 12))

    def login_user(self):
        """"сбор данных логина из GUI и проверка с перадресацией на вход"""
        answer = []
        user_name = str(self.welcome_window.lineEdit.text())
        password = self.welcome_window.lineEdit_2.text()
        if (len(user_name) > 0) and (len(password) > 0):

            answer = self.bd.login_user(user_name, password)  # возвращает все из бд
            if answer == []:
                self.welcome_window.label.setText('Такого пользователя нет')
                return
        else:
            return
        if (answer[0][2]) == password:
            if answer[0][5] == 1:
                self.admin_enterance()
            else:
                self.enterance(answer[0][3], answer[0][0])
        else:
            self.welcome_window.label.setText('Пароль неверный')

    def search_id(self):
        """Метод посика номера читателя по входным данным"""
        firs_name = self.aui.lineEdit_11.text()
        second_name = self.aui.lineEdit_12.text()
        users_looking_as_desc = self.bd.users_on_name(firs_name, second_name)

        if (len(users_looking_as_desc) == 1):
            id_reader = str(users_looking_as_desc[0][0])  #
            self.aui.lineEdit_13.setText(str(users_looking_as_desc[0][0]))
        else:
            self.aui.lineEdit_13.setText('')
            id_reader = None
        my_books = (self.bd.print_in_giu(self.bd.book_on_id_user(id_reader), 2))  #
        self.admin_out_table_my_books(my_books)  #

    def enterance(self, name, id_reader):  # сюда передовать имя и тд
        print(f"enterance")
        user_name = self.welcome_window.lineEdit.text()
        self.ui.label_6.setText(name)
        self.welcome_window.close()
        self.out_table(self.bd.print_in_giu(None, 0))
        my_books = (self.bd.print_in_giu(self.bd.book_on_id_user(id_reader), 2))
        self.out_table_my_books(my_books)
        self.ui.show()

    def admin_enterance(self):
        print(f"admin_enterance")
        self.out_table(self.bd.print_in_giu(None, 1))
        self.welcome_window.close()
        self.aui.show()
        completer = QCompleter(['Петр Николавич', 'Евгений Сыпало', 'Евгений Второй'])
        line_edit = self.aui.lineEdit_11

        line_edit.setCompleter(completer)
        completer.setCompletionMode(1)

    def index_changed(self):  # Вывод только необходимых строчек по количество авторов при добавлении
        count = int(self.aui.comboBox.currentText())
        print(f"index_changed {count}")
        if count == 1:
            self.aui.lineEdit_4.hide()
            self.aui.lineEdit_5.hide()
        if count == 2:
            self.aui.lineEdit_4.show()
            self.aui.lineEdit_5.hide()
        if count == 3:
            self.aui.lineEdit_4.show()
            self.aui.lineEdit_5.show()

    def text_field(self, text_err: str):
        print(f"text_field {text_err}")
        self.aui.label_4.setText(text_err)

    def visible_butt(self, visible):
        print(f"visible_butt {visible}")
        if visible == 1:
            self.aui.pushButton_2.show()
        else:
            self.aui.pushButton_2.hide()

    def check_data_adding_book(self):
        print(f"check_data_adding_book")
        data_on_adding=[(str(self.aui.lineEdit_3.text())), (str(self.aui.lineEdit.text())),
            (str(self.aui.lineEdit_2.text())), (str(self.aui.lineEdit_4.text())),
            (str(self.aui.lineEdit_5.text()))]
        count_author_in_ui=int(self.aui.comboBox.currentText())
        result = self.bd.check_adding(data_on_adding,count_author_in_ui)
        self.info(result)  # Ловим result и отправляем его в другую функцию, которая выводит на экран
        self.out_table(self.bd.print_in_giu(None, 1))

    def info(self, result):
        if result[0][0] == 0:
            self.print_succes(f'✅   Книга добавлена id {(result[1][0])}')
            return
        #       self.add_b.setText(f'Кнгига успешно добавлена id {result[0]}')
        # #     self.text_field('Успешно добавлено')
        #     self.visible_butt(0)
        elif result[0][0] == 1:
            #self.text_field('Пустое поле!')
            self.add_b.setText('Не заполнено поле')
        elif result[0][0] == 2:
            #self.text_field('Такая книга уже есть')
            self.add_b.setText(f'В базе уже есть книга с таким названием и id {result[0][1]}. Добавить еще одну?')
            self.add_b.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        elif result[0][0] == 3:
            self.add_b.setText(f'В базе нет такого автора {result[0][1]}. Добавить автора?')
            self.add_b.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            self.text_field('Такого автора нет ')
            #self.visible_butt(1)
        button=self.add_b.exec()
        self.dialog_result(button,result)

    def dialog_result(self,button,result):
        if button== QMessageBox.Ok and result[0][0]==3:# Это если на добавление автора
            print(result)
            self.bd.adding_writer(result[0][1])
            self.print_succes(f'✅       Автор {result[0][1]} добавлен')
        if button== QMessageBox.Ok and result[0][0]==2:#Это на дабавление такой же книги
            book_id=self.bd.adding_book(result[1],result[2])
            self.print_succes(f'✅   Книга добавлена id {book_id}')
        #self.out_table(self.bd.print_in_giu(None, 1))

    def search(self):
        search_text = str(self.ui.lineEdit.text())
        search_bool = int(self.ui.comboBox.currentIndex())
        kpk = self.bd.search_fetchall(search_text, search_bool)
        self.out_table(self.bd.print_in_giu(kpk, 0))

    def given_out(self):
        '''Функция выдачи книг'''
        texti = int(self.aui.tableWidget.item(self.aui.tableWidget.currentRow(), 0).text())
        print(texti)
        current_date = datetime.now().date()
        current_date_string = current_date.strftime('%d.%m.%Y')
        date_rev = self.aui.lineEdit_15.text()
        id_user = self.aui.lineEdit_13.text()
        if (date_rev != '..') and (id_user != ''):
            self.bd.giving_book(id_user, texti, current_date_string, date_rev)
            self.out_table(self.bd.print_in_giu(None, 1))
            my_books = (self.bd.print_in_giu(self.bd.book_on_id_user(id_user), 2))
            self.admin_out_table_my_books(my_books)
        else:
            self.err1.setWindowTitle('Ошибка выдачи')
            self.err1.setText('Не заполнены поля')
            self.err1.exec()

    def return_book(self):
        id_user = self.aui.lineEdit_13.text()
        if (id_user != '') and (self.aui.tableWidget_2.currentRow() != -1):
            id_book_row = int(self.aui.tableWidget_2.item(self.aui.tableWidget_2.currentRow(), 0).text())
            self.bd.return_book_bd(id_book_row)
            self.out_table(self.bd.print_in_giu(None, 1))
            my_books = (self.bd.print_in_giu(self.bd.book_on_id_user(id_user), 2))
            self.admin_out_table_my_books(my_books)
        else:
            self.err1.setWindowTitle('Ошибка ввода')
            self.err1.setText('Некоторые поля не заполнены или не выбрана книга')
            self.err1.exec()

    def admin_search(self):
        search_text = str(self.aui.lineEdit_14.text())
        search_bool = int(self.aui.comboBox_3.currentIndex())
        kpk = self.bd.search_fetchall(search_text, search_bool)
        self.out_table(self.bd.print_in_giu(kpk, 1))

    def log_out(self):
        self.ui.close()
        self.aui.close()
        self.welcome_window.show()

    def sample_deleting(self):
        texti = int(self.aui.tableWidget.item(self.aui.tableWidget.currentRow(), 0).text())
        self.err1.setWindowTitle('Удаление книги')
        book_on_delete_name = self.bd.exec_book_name_on_id(texti)
        text_message_err = str('Будет удалена Книга: "' + book_on_delete_name + '" c id: ' + str(texti))
        self.err1.setText(text_message_err)
        self.err1.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.err1.buttonClicked.connect(self.del_action)
        self.err1.exec()
        # self.bd.deletingt(texti)
        self.out_table(self.bd.print_in_giu(None, 1))
        # except AttributeError:
        #     print('мы в ошибке')
        #     self.err1.setWindowTitle('Ошибка удаления')
        #     self.err1.setText('Не выбраны поля')
        #     self.err1.exec()

    def del_action(self, btn):
        if btn.text() == 'OK':
            texti = int(self.aui.tableWidget.item(self.aui.tableWidget.currentRow(), 0).text())
            self.bd.deletingt(texti)
            print(texti)

    def ui_start(self):
        # app start
        print("UI preparing")
        self.aui.comboBox.currentIndexChanged.connect(self.index_changed)
        self.ui.lineEdit.textChanged.connect(self.search)
        self.aui.lineEdit_14.textChanged.connect(self.admin_search)
        self.aui.lineEdit_11.textChanged.connect(self.search_id)
        self.aui.lineEdit_12.textChanged.connect(self.search_id)
        self.aui.pushButton.clicked.connect(self.check_data_adding_book)
        #self.aui.pushButton_2.clicked.connect(self.add_data)
        self.aui.pushButton_3.clicked.connect(self.sample_deleting)
        self.aui.pushButton_5.clicked.connect(self.given_out)
        self.aui.pushButton_6.clicked.connect(self.return_book)
        self.ui.pushButton.clicked.connect(self.log_out)
        self.welcome_window.pushButton.clicked.connect(lambda: self.enterance("Тестировщик_читатель", 4))
        self.welcome_window.pushButton_3.clicked.connect(self.login_user)
        self.welcome_window.pushButton_2.clicked.connect(self.admin_enterance)
        self.welcome_window.show()
        print("UI app exec")
        self.app.exec()
