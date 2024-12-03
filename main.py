import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
DB_NAME = "coffee.sqlite"

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect(DB_NAME)
        self.pushButton.clicked.connect(self.adding)
        self.update_result()

    def update_result(self):
        query = """SELECT * FROM coffee"""
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'sort', 'degree', 'type',
             'description', 'price', 'size'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ui_file = io.StringIO(add_template)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect(DB_NAME)
        self.pushButton.clicked.connect(self.add_elem)
        self.__is_adding_successful = False  # переменная для правильного открытия и закрытия

    # Функция для добавления фильма в дб с проверкой правильности
    def add_elem(self):
        cur = self.con.cursor()
        print('asd')
        try:
            id = cur.execute("SELECT max(id) FROM coffee").fetchone()[0] + 1
            sort = self.sort.toPlainText()
            degree = self.degree.toPlainText()
            type = self.type.toPlainText()
            description = self.description.toPlainText()
            price = int(self.price.toPlainText())
            size = float(self.sizeOf.toPlainText())

            new_data = (id, sort, degree, type, description, price, size)
            print(new_data)
            cur.execute("INSERT INTO coffee VALUES (?,?,?,?,?,?,?)", new_data)
            self.__is_adding_successful = True
        except ValueError:
            self.__is_adding_successful = False

            self.statusBar().showMessage("Неверно заполнена форма")
        else:
            self.con.commit()
            self.parent().update_result()
            self.close()

    # Функция для проверки закрытия и открытия окна
    def get_adding_verdict(self):
        return self.__is_adding_successful

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec())
