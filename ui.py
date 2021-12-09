import sys, os, os.path, sqlite3
from datetime import time
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtWidgets

from database import *


# для обработки ошибок и перенаправлению потоков
def some_function():
    time.sleep(1)
    print("finished sleep, about to crash")
    raise RuntimeError("broken")


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()


        self.initUI()
        self.dbase = DataBase()



    """ начало блока описывающего весь интерфейс программы"""

    def initUI(self):

        self.resize(1280, 800)
        self.center()
        self.setWindowTitle("Арм Обходчик")
        # self.setGeometry(200, 200, 1150, 768)

        current_date = QDate.currentDate()
        time_now = QTime.currentTime()

        # определяем стиль шрифта для надписей и кнопок
        font_lbl = QFont()
        font_lbl.setPointSize(12)
        font_lbl.setBold(True)
        font_lbl.setWeight(75)

        # определяем шрифт для всех комбобоксов
        font_cbox = QFont()
        font_cbox.setPointSize(18)
        font_cbox.setBold(True)
        font_cbox.setWeight(80)

        # setGeometry(10, 100, 150, 30)   (отступ от левого края, ширина, отступ сверху, высота)

        # надпись дата
        self.lbl_date = QLabel("Дата", self)
        self.lbl_date.setText(current_date.toString(Qt.ISODate))
        self.lbl_date.setGeometry(250, 10, 150, 30)
        self.lbl_date.setFont(font_lbl)

        # надпись время
        # lbl_time = QLabel("Время", self)
        # lbl_time.setText(time.toString(Qt.DefaultLocaleLongDate))
        # lbl_time.setGeometry(375, 10, 150, 30)
        # lbl_time.setFont(font_lbl)

        # надпись смена
        self.lbl_shift = QLabel("Дневная смена", self)
        self.lbl_shift.setGeometry(400, 10, 200, 30)
        self.lbl_shift.setFont(font_lbl)

        # надпись информация
        self.lbl_info = QLabel("Информация", self)
        self.lbl_info.setGeometry(675, 10, 510, 30)
        self.lbl_info.setFont(font_lbl)

        # список выбора оператора
        self.cbox_operator = QComboBox(self)
        self.cbox_operator.setGeometry(QRect(40, 75, 400, 50))
        self.cbox_operator.setFont(font_cbox)

        # список выбора объекта проверки
        self.cbox_object = QComboBox(self)
        self.cbox_object.setGeometry(QRect(500, 75, 400, 50))
        self.cbox_object.setFont(font_cbox)

        # кнопка загрузки данных из файлов
        self.btn_addoperators = QPushButton("Загрузить данные", self)
        self.btn_addoperators.setGeometry(40, 5, 160, 40)
        self.btn_addoperators.clicked.connect(self.click_add_data)

        # кнопка загрузки списка объектов проверки из текстового файла
        # self.btn_addobjects = QPushButton("Загрузить список объектов", self)
        # self.btn_addobjects.setGeometry(230, 5, 200, 40)
        # self.btn_addobjects.clicked.connect(self.add_objects)

        # кнопка пролистывания списка вперед
        self.btn_next = QPushButton("Следующий", self)
        self.btn_next.setGeometry(1070, 300, 200, 65)
        self.btn_next.setFont(font_lbl)
        # self.btn_next.setEnabled(False)
        # self.btn_next.clicked.connect(self.get_objects)

        # кнопка пролистывания списка назад
        self.btn_prev = QPushButton("Предыдущий", self)
        self.btn_prev.setGeometry(1070, 390, 200, 65)
        self.btn_prev.setFont(font_lbl)
        # self.btn_prev.setEnabled(False)
        # self.btn_prev.clicked.connect(connect)

        # кнопка подтвержедния выбора оператора и объекта проверки
        self.btn_confirm = QPushButton("Подтвердить выбор", self)
        self.btn_confirm.setGeometry(1040, 75, 200, 65)
        self.btn_confirm.setFont(font_lbl)
        # self.btn_confirm.setEnabled(False)
        # используем lambda фукнцию т.к. она необходима для передач параметров
        self.btn_confirm.clicked.connect(self.add_params)

        self.btn_exit = QPushButton("Выход", self)
        self.btn_exit.clicked.connect(QApplication.instance().quit)
        self.btn_exit.setFont(font_lbl)
        self.btn_exit.setGeometry(1040, 700, 200, 65)

        self.btn_save = QPushButton("Сохранить результат", self)
        self.btn_save.setFont((font_lbl))
        self.btn_save.setGeometry(700, 700, 200, 65)
        self.btn_save.clicked.connect(self.save_results)

        # лист параметров проверки
        self.qlistw_params = QListWidget(self)
        self.qlistw_params.setGeometry(40, 150, 1000, 500)
        # self.list_params.resize(500, 500)
        self.qlistw_params.setStyleSheet('font-size: 30px;')

        # self.list_params.addItem(jan)
        # self.list_params.addItem(QListWidgetItem(jan))

        self.radiobtn_yes = QRadioButton('ДА', self)
        self.radiobtn_yes.setGeometry(400, 700, 200, 65)
        self.radiobtn_yes.setStyleSheet("QRadioButton"
                                        "{"
                                        "background-color : LightGreen"
                                        "} QRadioButton{font: 30pt Helvetica MS;}"
                                        "QRadioButton::indicator { width: 30px; height: 30px;}")

        self.radiobtn_no = QRadioButton('НЕТ', self)
        self.radiobtn_no.setGeometry(100, 700, 200, 65)
        self.radiobtn_no.setStyleSheet("QRadioButton"
                                       "{"
                                       "background-color : IndianRed"
                                       "} QRadioButton{font: 30pt Helvetica MS;}"
                                       "QRadioButton::indicator { width: 30px; height: 30px;}")

    """ конец блока описывающего весь интерфейс программы"""

    # положение окна программы
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # диалоговое окно выхода при закрытии формы на керстик
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # функция добавляем параметры проверки в окно в сооветсвии с выбраным объектов проверки в комбобоксе
    def add_params(self):
        self.qlistw_params.clear()
        dict_of_params = read_data_txt()  # функция из модуля files
        for key, value in dict_of_params.items():
            if key == self.cbox_object.currentText():
                print('Проверка функции add_params- ' + key, value)
                self.qlistw_params.addItems(value)

    # функция обрабокти кнопки Загрузить список операторов
    def add_operators(self):
        data = read_data_txt()  # функция из модуля files
        self.cbox_operator.clear()
        for key, value in data.items():
            if key == 'список операторов':
                self.cbox_operator.addItems(value)
                print('Проверка функции add_operators-', value)
                break
        if key != 'список операторов':
            QMessageBox.critical(self, 'Ошибка чтения данных', 'Отсутствует файл "список операторов.txt"')

    # функция обработки кнопки Загрузить список объектов
    def add_objects(self):
        data = read_data_txt()  # функция из модуля files
        self.cbox_object.clear()
        for key, value in data.items():
            if key == 'список объектов':
                self.cbox_object.addItems(value)
                print('Проверка функции add_objects-', value)
                break
        if key != 'список объектов':
            QMessageBox.critical(self, 'Ошибка чтения данных', 'Отсутствует файл "список объектов.txt"')

    def click_add_data(self):
        self.add_objects()
        self.add_operators()

    # функция проверка для консоли из files выводит словарь, где ключ название файла-объекта, а значенияя это параметры
    # проверки внутри
    def get_objects(self):
        dict_of_params = read_data_txt()  # функция из модуля files
        for keys, values in dict_of_params.items():
            print(keys, values)

    #запись выделенного параметра в базу данных и окрагиванием цвета в лист боксе
    def save_results(self):
        cbox_object = self.cbox_object.currentText()
        cbox_operator = self.cbox_operator.currentText()
        param = self.qlistw_params.currentItem()
        shift = self.lbl_shift.text()

        if param is not None:
            self.dbase.db_delete()  # функция из database.py
            self.dbase.db_connect()  # функция из database.py
            self.dbase.db_insert(param.text(), cbox_object,cbox_operator, shift) # функция из database.py
            param.setBackground(QColor("LightGreen"))  # устанавливаем цвет после записи в БД
            table_results = self.dbase.db_select()  # функция из database.py для для проверки
            for row in table_results:
                print('\nНаша таблица results БД db_results.db\n', row)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Не выбран параметр проверки!')

    # для обработки ошибок, чтобы окно не вылетало и т.д.
    def break_thread(self):
        test_thread = MadeToFail(self)
        test_thread.error_ocurred.connect(self.handle_error_ocurred)
        test_thread.start()

    # для обработки ошибок, чтобы окно не вылетало и т.д.
    def handle_error_ocurred(self, exception):
        print(exception)


# класс для обработки ошибок, чтобы окно не вылетало и т.д.
class MadeToFail(QThread):
    error_ocurred = pyqtSignal(Exception, name="errorOcurred")

    def run(self):
        try:
            some_function()
        except Exception as e:
            self.error_ocurred.emit(e)


def main():
    app = QApplication(sys.argv)

    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# старая фукнция
"""
    def test_add_params(self):
        folder = 'objects'  # присваиваем  директорию на ту где лежат файлы объектов
        for root, dirs, files in os.walk(folder):  # нас интересуют только файлы
            for filename in files:
                # при сравнеии удаляем расширение и оставляем только имя файла
                if (os.path.splitext(os.path.basename(filename))[0]) == self.win.lbl_parameter.setText():
                    filename = 'objects' + '\\' + filename  # присваиваем к имени файла ищи и путь
                    # откерываем файл и читаем по строкам, добавляем в список и работаем дальше
                    with open(filename, 'r') as file:
                        lines = file.read().split("\n")
                        file.close()

                        list_params = []
                        for line in lines:
                            list_params.append(line)
                        # удаляем пустые элементы в списке, если они есть
                        list_params[:] = [item for item in list_params if item != '']
                        # self.lbl_parameter.setText(list_params[1])  # временно выводим 1ю надпись для теста в лейбл
                        print(list_params)
"""
