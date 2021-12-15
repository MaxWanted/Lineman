"""Модуль описывает все окна программы и основной функционал"""

import sys, os, os.path, sqlite3
from datetime import time

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import *

from database import *
from random import randint


# для обработки ошибок и перенаправлению потоков
def some_function():
    time.sleep(1)
    print("finished sleep, about to crash")
    raise RuntimeError("broken")


"""|||||||||||||||||||||||||||||||||Класс описывает основное рабочее окно||||||||||||||||||||||||||||||||||"""


class MainWindow(QWidget):
    #    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.second_window = None
        self.setupUi()

    # функция описывает интерфейс программы
    def setupUi(self):

        self.resize(1280, 800)
        self.center()
        self.setWindowTitle('АРМ "Обходчик"')
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

        # кнопка подтвержедния выбора оператора и объекта проверки
        self.btn_confirm = QPushButton("Подтвердить выбор", self)
        self.btn_confirm.setGeometry(1040, 70, 200, 65)
        self.btn_confirm.setFont(font_lbl)
        # self.btn_confirm.setEnabled(False)
        # используем lambda фукнцию т.к. она необходима для передач параметров
        self.btn_confirm.clicked.connect(self.click_add_params)

        self.btn_exit = QPushButton("Выход", self)
        self.btn_exit.clicked.connect(QApplication.instance().quit)
        self.btn_exit.setFont(font_lbl)
        self.btn_exit.setGeometry(1040, 700, 200, 65)

        self.btn_save = QPushButton("Сохранить результат", self)
        self.btn_save.setFont(font_lbl)
        self.btn_save.setGeometry(700, 700, 200, 65)
        self.btn_save.clicked.connect(self.click_save_results)

        # лист параметров проверки
        self.qlistw_params = QListWidget(self)
        self.qlistw_params.setGeometry(40, 150, 1200, 500)
        # self.list_params.resize(500, 500)
        self.qlistw_params.setStyleSheet('font-size: 30px;')

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

    # функция  управляем открытием нового второго окна
    def show_second_window(self):
        if self.second_window is None:
            self.second_window = SecondWindow()
            self.second_window.show()
        else:
            self.second_window.close()
            self.second_window = None

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

    """||||||||||||||||||||||||||||||||блок основных функций||||||||||||||||||||||||||||||||||||||||"""

    # функция добавляем параметры проверки в окно в сооветсвии с выбраным объектов проверки в комбобоксе
    def click_add_params(self):  # кнопка "Подтверидть выбор"
        self.radiobtn_yes.setChecked(True)
        self.qlistw_params.clear()

        dict_of_params = read_data_txt()  # функция из модуля database
        for key, value in dict_of_params.items():
            if key == self.cbox_object.currentText():
                print('Проверка функции add_params- ' + key, value)
                self.qlistw_params.addItems(value)

    # функция обрабокти кнопки Загрузить список операторов
    def add_operators(self):
        data = read_data_txt()  # функция из модуля database
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
        data = read_data_txt()  # функция из модуля database
        self.cbox_object.clear()
        for key, value in data.items():
            if key == 'список объектов':
                self.cbox_object.addItems(value)
                print('Проверка функции add_objects-', value)
                break
        if key != 'список объектов':
            QMessageBox.critical(self, 'Ошибка чтения данных', 'Отсутствует файл "список объектов.txt"')

    def click_add_data(self):  # кнопка "Загрузить данные"
        self.add_objects()
        self.add_operators()

    # запись выделенного параметра в базу данных и окрагиванием цвета в лист боксе
    def click_save_results(self):
        cbox_object = self.cbox_object.currentText()
        cbox_operator = self.cbox_operator.currentText()
        param = self.qlistw_params.currentItem()
        shift = self.lbl_shift.text()


        if param is not None:
            # db_delete()  # функция из database.py
            db_connect()  # функция из database.py

            if self.radiobtn_yes.isChecked():  # если выбрано ДА
                db_insert(param.text(), cbox_object, cbox_operator, shift, checkout='Да')  # функция из database.py
                param.setBackground(QColor("LightGreen"))  # устанавливаем цвет после записи в БД
                table_results = db_select()  # функция из database.py для для проверки

            if self.radiobtn_no.isChecked():  # если выбрано НЕТ
                db_insert(param.text(), cbox_object, cbox_operator, shift, checkout='')
                param.setBackground(QColor("IndianRed"))
                table_results = db_select()  # функция из database.py для для проверки
                self.show_second_window()  # функция в этом классе

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


"""||||||||||||||||||Класс описывает второе окно несоответсвий||||||||||||||||||||||||||"""


class SecondWindow(QWidget):

    def __init__(self):
        super().__init__()

        # небольшой блок проверки, о том что каждый раз окно создается новоее.
        # layout = QVBoxLayout()
        # self.label = QLabel("Another Window % d" % randint(0, 100))
        # layout.addWidget(self.label)
        # self.setLayout(layout)
        self.setupUI()
        self.get_data()  # функция снова собирает данные из txt файлов в словарь и работает со спискмо несоответсвий
        # calling method

    def setupUI(self):

        self.resize(1280, 800)
        self.center()
        self.setWindowTitle('АРМ "Обходчик"')

        # определяем стиль шрифта для надписей и кнопок
        self.font_lbl = QFont()
        self.font_lbl.setPointSize(12)
        self.font_lbl.setBold(True)
        self.font_lbl.setWeight(75)

        # определяем шрифт для всех комбобоксов
        self.font_cbox = QFont()
        self.font_cbox.setPointSize(18)
        self.font_cbox.setBold(True)
        self.font_cbox.setWeight(80)

        # лист параметров проверки
        self.qlistw_defects = QListWidget(self)
        self.qlistw_defects.setGeometry(40, 40, 1000, 440)
        # self.list_params.resize(500, 500)
        self.qlistw_defects.setStyleSheet('font-size: 30px;')

        self.btn_save = QPushButton("Записать", self)
        self.btn_save.setGeometry(1070, 600, 200, 65)
        self.btn_save.setFont(self.font_lbl)
        # self.btn_next.setEnabled(False)
        self.btn_save.clicked.connect(self.click_save_results)

        self.btn_close = QPushButton("Закрыть форму", self)
        self.btn_close.clicked.connect(self.hide_second_window)
        self.btn_close.setGeometry(1070, 700, 200, 65)
        self.btn_close.setFont(self.font_lbl)
        # self.btn_prev.setEnabled(False)
        # self.btn_prev.clicked.connect(connect)

        self.btn_calendar = QPushButton("Каледнарь", self)
        # self.btn_close.clicked.connect(self.show_calendar)
        self.btn_calendar.setGeometry(1070, 500, 200, 65)
        self.btn_close.setFont(self.font_lbl)

        # список для комбобокса оценки последствий
        # при создании  списка  и  используем  строковые    литералы.
        list_consequences_grade = [
            self.tr('10'),
            self.tr('20'),
            self.tr('30'),
            self.tr('40'),
            self.tr('50'),
            self.tr('60'),
            self.tr('70'),
            self.tr('80'),
            self.tr('90'),
            self.tr('100')
        ]

        self.lbl_cons_grade = QLabel('Бальная оценка последствий', self)
        self.lbl_cons_grade.setFont(self.font_lbl)
        self.lbl_cons_grade.setGeometry(440, 570, 250, 50)
        # список с оценки последствий
        self.cbox_consequences_grade = QComboBox(self)
        self.cbox_consequences_grade.setGeometry(QRect(540, 620, 80, 50))
        self.cbox_consequences_grade.setFont(self.font_cbox)
        self.cbox_consequences_grade.clear()
        self.cbox_consequences_grade.addItems(list_consequences_grade)

        # список для комбобокса оценки несоответствий
        list_defect_grade = [
            self.tr('10'),
            self.tr('20'),
            self.tr('30'),
            self.tr('40'),
            self.tr('50'),
            self.tr('60'),
            self.tr('70'),
            self.tr('80'),
            self.tr('90'),
            self.tr('100')
        ]

        self.lbl_defect_grade = QLabel('Бальная оценка несоответствий', self)
        self.lbl_defect_grade.setFont(self.font_lbl)
        self.lbl_defect_grade.setGeometry(730, 570, 300, 50)

        # бальная оценка несоотвествий
        self.cbox_defect_grade = QComboBox(self)
        self.cbox_defect_grade.setGeometry(QRect(830, 620, 80, 50))
        self.cbox_defect_grade.setFont(self.font_cbox)
        self.cbox_defect_grade.clear()
        self.cbox_defect_grade.addItems(list_defect_grade)

        # текстовое поле воода для комментария
        self.lineEdit_comment = QLineEdit('Комментарий', self)
        self.lineEdit_comment.setPlaceholderText('Добавьте комментарий')
        self.lineEdit_comment.setGeometry(500, 700, 400, 60)

        self.lbllevel = QLabel("Уровень важности", self)
        self.lbllevel.setFont(self.font_lbl)
        self.lbllevel.setGeometry(1080, 30, 300, 65)
        # рисуем точки выбора уровней важности
        self.radiobtn_lowlvl = QRadioButton('Низкий', self)
        self.radiobtn_lowlvl.setGeometry(1070, 100, 200, 65)
        self.radiobtn_lowlvl.setStyleSheet("QRadioButton"
                                           "{"
                                           "background-color : LightGreen"
                                           "} QRadioButton{font: 26pt Helvetica MS;}"
                                           "QRadioButton::indicator { width: 30px; height: 30px;}")

        self.radiobtn_medlvl = QRadioButton('Средний', self)
        self.radiobtn_medlvl.setGeometry(1070, 200, 200, 65)
        self.radiobtn_medlvl.setStyleSheet("QRadioButton"
                                           "{"
                                           "background-color : Khaki"
                                           "} QRadioButton{font: 26pt Helvetica MS;}"
                                           "QRadioButton::indicator { width: 30px; height: 30px;}")

        self.radiobtn_hightlvl = QRadioButton('Высокий', self)
        self.radiobtn_hightlvl.setGeometry(1070, 300, 200, 65)
        self.radiobtn_hightlvl.setStyleSheet("QRadioButton"
                                             "{"
                                             "background-color : IndianRed"
                                             "} QRadioButton{font: 26pt Helvetica MS;}"
                                             "QRadioButton::indicator { width: 30px; height: 30px;}")

        # рисуем точки выбора выявления несоответсвий и далее помещаем их в групп бокс
        self.radiobtn_visual_incpect = QRadioButton('Визуальный осмотр', self)
        self.radiobtn_visual_incpect.setGeometry(40, 500, 400, 65)
        self.radiobtn_visual_incpect.setStyleSheet("QRadioButton{font: 16pt Helvetica MS;}"
                                                   "QRadioButton::indicator { width: 30px; height: 30px;}")

        self.radiobtn_device_incpect = QRadioButton('Диагностика приборами', self)
        self.radiobtn_device_incpect.setGeometry(350, 500, 400, 65)
        self.radiobtn_device_incpect.setStyleSheet("QRadioButton{font: 16pt Helvetica MS;}"
                                                   "QRadioButton::indicator { width: 30px; height: 30px;}")

        self.radiobtn_test_incpect = QRadioButton('Испытание', self)
        self.radiobtn_test_incpect.setGeometry(700, 500, 400, 65)
        self.radiobtn_test_incpect.setStyleSheet("QRadioButton{font: 16pt Helvetica MS;}"
                                                 "QRadioButton::indicator { width: 30px; height: 30px;}")

        # тут прописывает групбоксы для наших радио кнопок осмотра
        self.grbox_rbtninspect = QButtonGroup()
        self.grbox_rbtninspect.addButton(self.radiobtn_visual_incpect)  # 0 индекс
        self.grbox_rbtninspect.addButton(self.radiobtn_device_incpect)  # 1 индекс
        self.grbox_rbtninspect.addButton(self.radiobtn_test_incpect)  # 2 индекс

        # для кнопок уровня важности проверки
        self.grbox_rbtnlvl = QButtonGroup()
        self.grbox_rbtnlvl.addButton(self.radiobtn_lowlvl)
        self.grbox_rbtnlvl.addButton(self.radiobtn_medlvl)
        self.grbox_rbtnlvl.addButton(self.radiobtn_hightlvl)

        current_date = datetime.now()
        self.edit_solve_date = QDateEdit(self)
        self.edit_solve_date.setGeometry(50, 620, 200, 80)
        self.edit_solve_date.setFont(self.font_lbl)
        # d = (current_time.strftime('%m/%d/%Y'))
        self.edit_solve_date.setDate(current_date)

    def hide_second_window(self):  # кнопка закрыть форму на дочерней форме
        # self.check_visibility() #проверяем главное окно на отображение и показываем
        self.hide()  # закрываем текущую форму

    def check_visibility(self):
        if self.mainwin.isVisible():
            self.mainwin.hide()
            print("Форма типа спряталась")
        else:
            self.mainwin.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_data(self):
        dict_of_params = read_data_txt()  # функция из модуля database
        for keys, values in dict_of_params.items():
            print(keys, values)
            if keys == 'список несоответствий':
                self.qlistw_defects.addItems(values)
                break
        if keys != 'список несоответствий':
            QMessageBox.critical(self, 'Ошибка чтения данных', 'Отсутствует файл "список несоответствий.txt"')

    def click_save_results(self):
        defect = self.qlistw_defects.currentItem()
        defect_grade = self.cbox_defect_grade.currentText()
        cons_grade = self.cbox_consequences_grade.currentText()
        detection_type = self.find_checked_rbtn_inspect()
        importance_lvl = self.find_checked_rbtn_lvl()
        comment = self.lineEdit_comment.text()
        solve_date = self.edit_solve_date.text()


        if defect is not None:
            # db_delete()  # функция из database.py
            db_connect()  # функция из database.py
            db_insert_defects(defect.text(), defect_grade, cons_grade, detection_type,
                              importance_lvl, comment, solve_date, checkout='Нет')  # функция из database.py
            table_results = db_select()  # функция из database.py для для проверки
            # self.hide_second_window()  # функция в этом классе
            for row in table_results:
                print('\nНаша таблица с добавлением results БД db_results.db\n', row)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Не выбран дефект\несоответствие!')

    # функция возвращает имя выбранного элементы осмотра radiobutton
    def find_checked_rbtn_inspect(self):
        # перебираем наши radiobuttons в groupbox и получаем их порядковые номера
        checklist = ([i for i, button in enumerate(self.grbox_rbtninspect.buttons()) if button.isChecked()])
        for c in checklist:
            if c == 0:
                return 'Визуальный осмотр'
            if c == 1:
                return 'Диагностика приборами'
            if c == 2:
                return 'Испытание'

    def find_checked_rbtn_lvl(self):
        checklist = ([i for i, button in enumerate(self.grbox_rbtnlvl.buttons()) if button.isChecked()])
        for c in checklist:
            if c == 0:
                return 'Низкий'
            if c == 1:
                return 'Средний'
            if c == 2:
                return 'Высокий'


# класс для обработки ошибок, управление потоком
class MadeToFail(QThread):
    error_ocurred = pyqtSignal(Exception, name="errorOcurred")

    def run(self):
        try:
            some_function()
        except Exception as e:
            self.error_ocurred.emit(e)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
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
