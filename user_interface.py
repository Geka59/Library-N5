from PyQt5 import QtWidgets, uic,QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from database import Database
from datetime import datetime

class UserInterface:
    app = None
    aui = None
    ui = None
    welcome_window = None

    def __init__(self):
        # init
        app = QtWidgets.QApplication([])
        welcome_window = uic.loadUi("assets\WelcomeWindow.ui")
        welcome_window.setWindowTitle("Вход")
        aui: object = uic.loadUi("assets\AdminWindow.ui")
        ui = uic.loadUi("assets\WindowMain.ui")
        ui.setWindowTitle("Library № 5")  # Начальные настройки фронта
        aui.pushButton_2.hide()
        aui.comboBox.addItems(['1', '2', '3'])
        ui.comboBox.addItems(['Авторы', 'Книги'])
        aui.comboBox_3.addItems(['Авторы', 'Название'])

        aui.lineEdit_4.hide()
        aui.lineEdit_5.hide()

        print("UI Init complited")

        self.app = app
        self.ui = ui
        self.aui = aui
        self.welcome_window = welcome_window

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
        self.aui.tableWidget.setHorizontalHeaderLabels(['id книги', 'Название', 'Автор', 'Краткое описание','Читатель','Дата выдачи','Дата возврата'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.aui.tableWidget.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
                if y==6 and str(rows[x][y])!=''and self.data_revision(str(rows[x][y])):
                    self.setColortoRow(x,1)
        self.aui.tableWidget.resizeColumnsToContents()

    def out_table_my_books(self,rows):
        """вывод в окно моих книг"""
        self.ui.tableWidget_2.setRowCount(len(rows))
        self.ui.tableWidget_2.setColumnCount(6)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(
            ['id книги', 'Название', 'Автор', 'Краткое описание','дата выдачи','дата возврата'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.ui.tableWidget_2.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
                if y==5 and self.data_revision(str(rows[x][y])):
                    self.setColortoRow(x,0)
        self.ui.tableWidget_2.resizeColumnsToContents()




    def data_revision(self,date_for_revision):
        current_date = datetime.now().date()
        current_date_string = current_date.strftime('%d.%m.%Y')
        a = (datetime.strptime(date_for_revision, '%d.%m.%Y')).date()
        if(current_date>a):
            return True

    def setColortoRow(self, rowIndex,flag):
        if flag==0:
            for j in range(self.ui.tableWidget_2.columnCount()):
                self.ui.tableWidget_2.item(rowIndex, j).setBackground(QtGui.QColor(204,255,0))
        else:
            for j in range(self.aui.tableWidget.columnCount()):
               self.aui.tableWidget.item(rowIndex, j).setBackground(QtGui.QColor(204,255,0))

    def login_user(self):
        """"сбор данных логина из GUI и проверка с перадресацией на вход"""
        answer=[]
        user_name = str(self.welcome_window.lineEdit.text())
        password = self.welcome_window.lineEdit_2.text()
        if (len(user_name)>0) and (len(password)>0):
            bd=Database()
            answer=bd.login_user(user_name,password) # возвращает все из бд
            if answer==[]:
                self.welcome_window.label.setText('Такого пользователя нет')
                return
        else:
            return
        if(answer[0][2])==password:
            if answer[0][5]==1:
                self.admin_enterance()
            else:
                self.enterance(answer[0][3],answer[0][0])
        else:
            self.welcome_window.label.setText('Пароль неверный')

    def search_id(self):
        """Метод посика номера читателя по входным данным"""
        firs_name=self.aui.lineEdit_11.text()
        second_name=self.aui.lineEdit_12.text()
        bd=Database()
        users_looking_as_desc=bd.users_on_name(firs_name,second_name)
        if(len(users_looking_as_desc)==1):
            self.aui.lineEdit_13.setText(str(users_looking_as_desc[0][0]))


    def enterance(self,name,id_reader):# сюда передовать имя и тд
        print(f"enterance")
        user_name=self.welcome_window.lineEdit.text()
        self.ui.label_6.setText(name)
        self.welcome_window.close()
        bd=Database()
        self.out_table(bd.print_in_giu(None,0))
        my_books=(bd.print_in_giu(bd.book_on_id_user(id_reader),2))
        self.out_table_my_books(my_books)
        self.ui.show()

    def admin_enterance(self):
        print(f"admin_enterance")
        bd = Database()
        self.out_table(bd.print_in_giu(None,1))
        self.welcome_window.close()
        self.aui.show()

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

    def check_data(self):
        print(f"check_data")
        bd = Database()
        result = bd.check_adding(
                            (str(self.aui.lineEdit_3.text())), (str(self.aui.lineEdit.text())),
                            (str(self.aui.lineEdit_2.text())), (str(self.aui.lineEdit_4.text())),
                            (str(self.aui.lineEdit_5.text())), int(self.aui.comboBox.currentText()))
        self.out_table(bd.print_in_giu(None,1))

        self.info(result)# Ловим result и отправляем его в другую функцию, которая выводит на экран


    def info(self,result):
        if result==0:
            self.text_field('Успешно добавлено')
            self.visible_butt(0)
        elif result==1:
            self.text_field('Пустое поле!')
        elif result==2:
            self.text_field('Такая книга уже есть')
        elif result==3:
            self.text_field('Такого автора нет ')
            self.visible_butt(1)

    def add_data(self):
        print(f"add_data")
        self.visible_butt(0)
        bd = Database()
        return bd.adding_writer(
                             (str(self.aui.lineEdit_2.text())),
                             (str(self.aui.lineEdit_4.text())),
                             (str(self.aui.lineEdit_5.text())),
                             int(self.aui.comboBox.currentText()))
    def search(self):
        search_text=str(self.ui.lineEdit.text())
        search_bool = int(self.ui.comboBox.currentIndex())
        bd=Database()
        kpk=bd.search_fetchall(search_text,search_bool)
        self.out_table(bd.print_in_giu(kpk,0))

    def admin_search(self):
        search_text=str(self.aui.lineEdit_14.text())
        search_bool = int(self.aui.comboBox_3.currentIndex())
        bd=Database()
        kpk=bd.search_fetchall(search_text,search_bool)
        self.out_table(bd.print_in_giu(kpk,1))


    def log_out(self):
        self.ui.close()
        self.aui.close()
        self.welcome_window.show()

    def sample_deleting(self):
        try:
            texti=int(self.aui.tableWidget.item(self.aui.tableWidget.currentRow(), 0).text())
            print(texti)
            bd=Database()
            bd.deletingt(texti)
            self.out_table(bd.print_in_giu(None,1))
        except AttributeError:
            print('мы в ошибке')


    def ui_start(self):
        # app start
        print("UI preparing")
        self.aui.comboBox.currentIndexChanged.connect(self.index_changed)
        self.ui.lineEdit.textChanged.connect(self.search)
        self.aui.lineEdit_14.textChanged.connect(self.admin_search)
        self.aui.lineEdit_11.textChanged.connect(self.search_id)
        self.aui.lineEdit_12.textChanged.connect(self.search_id)
        self.aui.pushButton.clicked.connect(self.check_data)
        self.aui.pushButton_2.clicked.connect(self.add_data)
        self.aui.pushButton_3.clicked.connect(self.sample_deleting)
        self.ui.pushButton.clicked.connect(self.log_out)
        self.welcome_window.pushButton.clicked.connect(lambda :self.enterance("Тестировщик_читатель",4))
        self.welcome_window.pushButton_3.clicked.connect(self.login_user)
        self.welcome_window.pushButton_2.clicked.connect(self.admin_enterance)
        self.welcome_window.show()
        print("UI app exec")
        self.app.exec()
