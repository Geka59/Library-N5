from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from database import Database


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
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(['id книги', 'Название', 'Автор', 'Краткое описание'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.ui.tableWidget.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
        self.ui.tableWidget.resizeColumnsToContents()
        """вывод в окно админа"""
        self.aui.tableWidget.setRowCount(len(rows))
        self.aui.tableWidget.setColumnCount(4)
        self.aui.tableWidget.setHorizontalHeaderLabels(['id книги', 'Название', 'Автор', 'Краткое описание'])
        for x in range(0, len(rows)):
            for y in range(len(rows[x])):
                self.aui.tableWidget.setItem(x, y, QTableWidgetItem(str(rows[x][y])))
        self.aui.tableWidget.resizeColumnsToContents()

    def enterance(self):
        print(f"enterance")
        user_name=self.welcome_window.lineEdit.text()
        self.ui.label_6.setText(user_name)
        self.welcome_window.close()
        bd=Database()
        self.out_table(bd.print_in_giu(None))
        self.ui.show()

    def admin_enterance(self):
        print(f"admin_enterance")
        bd = Database()
        self.out_table(bd.print_in_giu(None))
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
        self.out_table(bd.print_in_giu(None))

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
        self.out_table(bd.print_in_giu(kpk))


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
            self.out_table(bd.print_in_giu(None))
        except AttributeError:
            print('мы в ошибке')


    def ui_start(self):
        # app start
        print("UI preparing")
        self.aui.comboBox.currentIndexChanged.connect(self.index_changed)
        self.ui.lineEdit.textChanged.connect(self.search)
        self.aui.pushButton.clicked.connect(self.check_data)
        self.aui.pushButton_2.clicked.connect(self.add_data)
        self.aui.pushButton_3.clicked.connect(self.sample_deleting)
        self.ui.pushButton.clicked.connect(self.log_out)
        self.welcome_window.pushButton.clicked.connect(self.enterance)
        self.welcome_window.pushButton_2.clicked.connect(self.admin_enterance)
        self.welcome_window.show()
        print("UI app exec")
        self.app.exec()
