"""Модуль описывает два рабочих окна программы и основной функционал"""

import sys, os, os.path, sqlite3
from datetime import time
from idlelib import window

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui, QtCore

from database import *
from authorization import *
from random import randint


# для обработки ошибок и перенаправлению потоков
def some_function():
    time.sleep(1)
    print("finished sleep, about to crash")
    raise RuntimeError("broken")


"""|||||||||||||||||||||||||||||||||Класс описывает основное рабочее окно||||||||||||||||||||||||||||||||||
param - параметр проверки 
cbox_object - объект проверки
cbox_operator  - оператор
shift - текущая смена
checkout -  состояние проверки ДА или НЕТ
"""


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.second_window = None  # для отображеняи 2го окна. функция show_second_window
        self.login_window = None
        self.setupUi()  # генерирует интерфейс
        self.check_shift()  # определяет текущую смену в зависимости от времени
        self.show_login_form()  # показывает окно авторизации при открытии программы

        # self.setStyleSheet('background-color: #DCDCDC')

    # функция описывает интерфейс программы
    def setupUi(self):

        qss_file = open('style_file.css').read()
        self.resize(1280, 800)
        self.setFixedSize(1280, 800)
        self.center()
        self.setWindowTitle('АРМ "Обходчик - система контроля состояния оборудования"')

        # self.setGeometry(200, 200, 1150, 768)

        date = datetime.today()
        current_date = str(date.strftime('%d.%m.%Y'))

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

        self.font_info = QFont()
        self.font_info.setPointSize(12)
        self.font_info.setItalic(True)
        self.font_info.setWeight(75)

        # setGeometry(10, 100, 150, 30)   (отступ от левого края, ширина, отступ сверху, высота)

        # надпись дата
        self.lbl_date = QLabel("Дата", self)
        self.lbl_date.setText(current_date)
        self.lbl_date.setGeometry(150, 5, 100, 30)
        self.lbl_date.setStyleSheet('border: 1px solid rgb(220, 220, 220); border-radius: 2px;')
        self.lbl_date.setAlignment((Qt.AlignHCenter | Qt.AlignTop))
        self.lbl_date.setFont(font_lbl)

        # надпись смена
        self.lbl_shift = QLabel("Дневная смена", self)
        self.lbl_shift.setGeometry(290, 5, 150, 30)
        self.lbl_shift.setStyleSheet('border: 1px solid rgb(220, 220, 220); border-radius: 2px;')
        self.lbl_shift.setAlignment((Qt.AlignHCenter | Qt.AlignTop))
        self.lbl_shift.setFont(font_lbl)

        # надпись информация
        self.lbl_info = QLabel('Нажмите "Загрузить данные" ', self)
        self.lbl_info.setGeometry(500, 5, 400, 30)
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setStyleSheet('border: 1px solid rgb(220, 220, 220); border-radius: 2px;')
        self.lbl_info.setAlignment((Qt.AlignHCenter | Qt.AlignTop))
        self.lbl_info.setFont(self.font_info)

        self.lbl_oper = QLabel('<h3 style="color: rgb(0, 121, 194)">Оператор</h3> ', self)
        self.lbl_oper.setGeometry(40, 60, 200, 20)
        # список выбора оператора
        self.cbox_operator = QComboBox(self)
        self.cbox_operator.setGeometry(QRect(40, 80, 400, 50))
        self.cbox_operator.setFont(font_cbox)

        self.lbl_obj = QLabel('<h3 style="color: rgb(0, 121, 194)">Объект проверки</h3> ', self)
        self.lbl_obj.setGeometry(500, 60, 200, 20)
        # список выбора объекта проверки
        self.cbox_object = QComboBox(self)
        self.cbox_object.setGeometry(QRect(500, 80, 400, 50))
        self.cbox_object.setFont(font_cbox)

        # о программе
        self.btn_about = QPushButton("?", self)
        self.btn_about.setGeometry(10, 5, 20, 30)
        #self.btn_about.setIcon(QIcon('icons/download.png'))
        #self.btn_about.setIconSize(QSize(25, 25))
        self.btn_about.clicked.connect(self.about)
        self.btn_about.setStyleSheet("font: bold")

        # помощь
        self.btn_help = QPushButton("Помощь", self)
        self.btn_help.setGeometry(40, 5, 75, 30)
        # self.btn_about.setIcon(QIcon('icons/download.png'))
        # self.btn_about.setIconSize(QSize(25, 25))
        self.btn_help.clicked.connect(self.help)
        self.btn_help.setStyleSheet("font: bold")


        # кнопка загрузки данных из файлов
        self.btn_loaddata = QPushButton("  Загрузить данные", self)
        self.btn_loaddata.setGeometry(1020, 5, 220, 40)
        self.btn_loaddata.setIcon(QIcon('icons/download.png'))
        self.btn_loaddata.setIconSize(QSize(25, 25))
        self.btn_loaddata.clicked.connect(self.click_add_data)
        self.btn_loaddata.setStyleSheet("font: bold")

        # кнопка подтвержедния выбора оператора и объекта проверки
        self.btn_confirm = QPushButton("  Подтвердить выбор", self)
        self.btn_confirm.setGeometry(1020, 70, 220, 65)
        self.btn_confirm.setEnabled(False)
        self.btn_confirm.setFont(font_lbl)
        self.btn_confirm.setIcon(QIcon('icons/confirm.png'))
        self.btn_confirm.setIconSize(QSize(25, 25))  # )
        # используем lambda фукнцию т.к. она необходима для передач параметров
        self.btn_confirm.clicked.connect(self.click_add_params)

        self.btn_exit = QPushButton("  Выход", self)
        # self.btn_exit.clicked.connect(QApplication.instance().quit)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setFont(font_lbl)
        self.btn_exit.setIcon(QIcon('icons/exit.png'))
        self.btn_exit.setIconSize(QSize(25, 25))
        self.btn_exit.setGeometry(1040, 700, 200, 65)

        self.btn_save = QPushButton("  Записать", self)
        self.btn_save.setFont(font_lbl)
        self.btn_save.setGeometry(700, 700, 200, 65)
        self.btn_save.setIcon(QIcon('icons/save.png'))
        self.btn_save.setIconSize(QSize(25, 25))
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.click_save_results)

        self.lbl_params = QLabel('<h3 style="color: rgb(0, 121, 194)">Параметры проверки </h3> ', self)
        self.lbl_params.setGeometry(40, 150, 200, 20)
        # лист параметров проверки
        self.qlistw_params = QListWidget(self)
        self.qlistw_params.setGeometry(40, 170, 1200, 500)
        # self.list_params.resize(500, 500)
        self.qlistw_params.setStyleSheet('font-size: 30px;')

        self.lbl_yes_no = QLabel('<h3 style="color: rgb(0, 121, 194)">Проверка соответствия</h3> ', self)
        self.lbl_yes_no.setGeometry(40, 670, 200, 20)

        self.radiobtn_yes = QRadioButton('ДА', self)
        self.radiobtn_yes.setGeometry(400, 700, 200, 65)

        self.lblyes = QLabel(self)
        self.lblyes.setStyleSheet("background-color : LightGreen")
        self.lblyes.setGeometry(400, 760, 100, 10)

        self.radiobtn_no = QRadioButton('НЕТ', self)
        self.radiobtn_no.setGeometry(150, 700, 200, 65)

        self.lblno = QLabel(self)
        self.lblno.setStyleSheet("background-color : IndianRed")
        self.lblno.setGeometry(150, 760, 100, 10)

        self.btn_confirm.setStyleSheet(qss_file)
        self.btn_exit.setStyleSheet(qss_file)
        self.btn_save.setStyleSheet(qss_file)
        self.btn_loaddata.setStyleSheet(qss_file)
        self.radiobtn_yes.setStyleSheet(qss_file)
        self.radiobtn_no.setStyleSheet(qss_file)


    # кнопка ? о программе
    def about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('О программе')
        msg.setText('Приложение АРМ "Обходчик" - организация обходов и осмотров состояния оборудования в ЮФ ООО '
                    '"Газпром энерго". Ведение статистики дефектов и единой базы несоответствий.\n\n' 
                    'Деркач М.А. - программист 2 кат. отдела ВСЭиР ИУСиС\nm.a.derkach@gmail.com'
                    '\n\nТекущая версия  - Python, 2021\nОригинальная версия - VBA, 2020')
        msg.exec_()

    def help(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Справка')
        msg.setText('Нажмите кнопку "Загрузить данные", чтобы программа прочитала файлы несоответсвий, объектов и '
                    'операторов.\nДалее нажмите кнопку "Подтвердить выбор", для загрузки этих данных в программу.\n'
                    'Нажимайте на строки с параметрами проверки в главном окне, выбирайте переключатель проверки "ДА"'
                    'или "НЕТ" и нажимайте кнопку "Записать".\n\nЕсли будет выбран переключатель "НЕТ", то откроется'
                    'другое окно с выбором несоответствий и сопутствующих параметров. После выбора несоответствий в '
                    'новом окне, нажмите кнопку "Записать", окно закроется и вы снова сможете продолжить работу с '
                    'первой формой.\n\nДля корректного завершения работы программыи сохранения всех записанных данных'
                    'нажимайте кнопку "Выход" из главной формы')
        msg.exec_()

    # функция оперделяет  дневную или ночную смену  от 8 до 20 часов
    def check_shift(self):
        now = datetime.now()
        if time(8) <= now.time() <= time(20):
            self.lbl_shift.setText('Дневная смена')
        else:
            self.lbl_shift.setText('Ночная смена')

    # функция  управляем открытием нового второго окна
    def show_second_window(self):
        if self.second_window is None:
            self.second_window = SecondWindow()
            self.second_window.show()
        else:
            self.second_window.close()
            self.second_window = None

    def show_login_form(self):
        if self.login_window is None:
            self.login_window = LoginForm()
            self.login_window.show()
        else:
            self.login_window.close()
            self.lbl_info = None

    # положение окна программы
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # диалоговое окно выхода при закрытии формы на керстик
    def closeEvent(self, event):
        date = datetime.today()
        current_date = str((date.strftime('%d.%m.%Y %H:%M')))
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Уверены? Все несохранённые данные будут потеряны!", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            with open('temp/logs.txt', 'a') as file:
                file.write(current_date + ' завершение работы программы' + '\n')
        else:
            event.ignore()

    """||||||||||||||||||||||||||||||||блок основных функций||||||||||||||||||||||||||||||||||||||||"""

    # функция добавляем параметры проверки в окно в сооветсвии с выбраным объектов проверки в комбобоксе
    def click_add_params(self):  # кнопка "Подтверидть выбор"
        self.radiobtn_yes.setChecked(True)
        self.btn_save.setEnabled(True)
        self.lbl_info.setText('Выберите параметр проверки и нажмите "Записать"')
        self.qlistw_params.clear()

        dict_of_params = read_data_txt()  # функция из модуля database
        for key, value in dict_of_params.items():
            if key == self.cbox_object.currentText():
                print('Проверка функции add_params- ' + key, value)
                self.qlistw_params.addItems(value)

    # функция загурзки выбранного оператора при автворизации чыерез буферный txt файл
    def add_operators(self):
        with open('temp/buffer_operator.txt', 'r') as file:
            oper = file.readline()
            self.cbox_operator.addItem(oper)

    # функция обработки кнопки Загрузить список объектов
    def add_objects(self):
        data = read_data_txt()  # функция из модуля database
        self.cbox_object.clear()
        for key, value in data.items():
            if key == 'список объектов':
                self.cbox_object.addItems(value)
                # print('Проверка функции add_objects-', value)
                self.btn_loaddata.setEnabled(False)
                msg = '---\t' + '\n---\t'.join(value)
                QMessageBox.information(self, "Объекты загружены", msg, QMessageBox.Ok)
                break
        if key != 'список объектов':
            QMessageBox.critical(self, 'Ошибка чтения данных', 'Отсутствует файл "список объектов.txt"')

    def click_add_data(self):  # кнопка "Загрузить данные"
        date = datetime.today()
        current_date = str((date.strftime('%d.%m.%Y %H:%M')))
        db_connect()  # функция соаздния БД из модуля database.py
        self.add_objects()
        if self.cbox_object.currentText() and self.cbox_operator.currentText() is not None:
            self.lbl_info.setText('Операторы и объекты успешно загружены')
            self.add_operators()
            self.btn_confirm.setEnabled(True)

    # запись выделенного параметра в базу данных и окрагиванием цвета в лист боксе
    def click_save_results(self):
        cbox_object = self.cbox_object.currentText()
        cbox_operator = self.cbox_operator.currentText()
        param = self.qlistw_params.currentItem()
        shift = self.lbl_shift.text()
        self.lbl_info.setText('')

        # if param is not None:
        if self.qlistw_params.selectedItems():  # если  выбран парметр проверки к листбоксе
            # db_delete()  # функция из database.py
            # db_connect()  # функция из database.py

            if self.radiobtn_yes.isChecked():  # если выбрано ДА
                db_insert(param.text(), cbox_object, cbox_operator, shift, checkout='Да')  # функция из database.py
                param.setBackground(QColor("LightGreen"))  # устанавливаем цвет после записи в БД
                param.setFlags(Qt.NoItemFlags)  # блокируем записанный элемент
                # table_results = db_select()  # функция из database.py для для проверки
                self.lbl_info.setText('Данные записаны')

            if self.radiobtn_no.isChecked():  # если параметр проверки выбран НЕТ
                param.setBackground(QColor("IndianRed"))
                param.setFlags(Qt.NoItemFlags)  # блокируем записанный элемент
                #  добавляем в БД запись, но уже с проверкой "НЕТ" и далее работаем с окном несоотвествий
                db_insert(param.text(), cbox_object, cbox_operator, shift, checkout='Нет')
                self.show_second_window()  # функция в этом классе
                self.lbl_info.setText('Данные несоответствий записаны')
        else:
            QMessageBox.critical(self, 'Ошибка', 'Не выбран параметр проверки!')

        # чисто печать БД в консоль во время отладки
        table_results = db_select()
        for row in table_results:
            print('\nНаша таблица results БД db_results.db\n', row)

    # для обработки ошибок, чтобы окно не вылетало и т.д.
    def break_thread(self):
        test_thread = MadeToFail(self)
        test_thread.error_ocurred.connect(self.handle_error_ocurred)
        test_thread.start()

    def handle_error_ocurred(self, exception):
        print(exception)


"""||||||||||||||||||Класс описывает второе окно несоответсвий||||||||||||||||||||||||||

defect - дефект во втором окне несоответствий
defect_grade -  бальная оценка несоответсвий
cons_grade - бальная оценка последствий
detection_type - дата обнаружения
importance_lvl - уровень важности
comment - комментарий на второй форме
solve_date  - дата устранения 
"""


class SecondWindow(QWidget):

    def __init__(self):
        super().__init__()

        # небольшой блок проверки, который доказывает что каждый раз окно создается новое.
        # layout = QVBoxLayout()
        # self.label = QLabel("Another Window % d" % randint(0, 100))
        # layout.addWidget(self.label)
        # self.setLayout(layout)
        self.setupUI()
        self.get_data()  # функция снова собирает данные из txt файлов в словарь и работает со спискмо несоответсвий

    def setupUI(self):

        qss_file = open('style_file.css').read()
        self.resize(1280, 800)
        self.setFixedSize(1280, 800)

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

        # надпись информация
        self.lbl_info = QLabel('<h2 style="color: rgb(0, 121, 194)">Выберите тип несоответствия</h2> ', self)
        self.lbl_info.setGeometry(40, 5, 1000, 30)
        self.lbl_info.setAlignment((Qt.AlignHCenter | Qt.AlignTop))
        self.lbl_info.setFont(self.font_lbl)

        # лист параметров проверки
        self.qlistw_defects = QListWidget(self)
        self.qlistw_defects.setGeometry(40, 40, 1000, 440)
        # self.list_params.resize(500, 500)
        self.qlistw_defects.setStyleSheet('font-size: 30px;')

        icon = QIcon()
        self.btn_save = QPushButton(" Записать", self)
        icon.addFile('icons/save.png')
        self.btn_save.setIcon(icon)
        self.btn_save.setIconSize(QSize(25, 25))
        self.btn_save.setGeometry(1070, 600, 200, 65)
        self.btn_save.setFont(self.font_lbl)
        self.btn_save.clicked.connect(self.click_save_results)

        self.btn_close = QPushButton(" Закрыть форму", self)
        self.btn_close.clicked.connect(self.hide_second_window)
        self.btn_close.setIcon(QIcon('icons/exit.png'))
        self.btn_close.setIconSize(QSize(25, 25))
        self.btn_close.setGeometry(1070, 700, 200, 65)
        self.btn_close.setFont(self.font_lbl)
        self.btn_close.setEnabled(False)

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
        self.lbl_cons_grade.setStyleSheet('border: 1px solid rgb(220, 220, 220); border-radius: 2px;')
        self.lbl_cons_grade.setGeometry(440, 580, 260, 40)
        # список с оценки последствий
        self.cbox_consequences_grade = QComboBox(self)
        self.cbox_consequences_grade.setGeometry(QRect(540, 630, 80, 50))
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
        self.lbl_defect_grade.setStyleSheet('border: 1px solid rgb(220, 220, 220); border-radius: 2px;')
        self.lbl_defect_grade.setGeometry(730, 580, 300, 40)

        # бальная оценка несоотвествий
        self.cbox_defect_grade = QComboBox(self)
        self.cbox_defect_grade.setGeometry(QRect(830, 630, 80, 50))
        self.cbox_defect_grade.setFont(self.font_cbox)
        self.cbox_defect_grade.clear()
        self.cbox_defect_grade.addItems(list_defect_grade)

        # текстовое поле воода для комментария
        self.lineEdit_comment = QLineEdit('Комментарий', self)
        # self.lineEdit_comment.setPlaceholderText('Добавьте комментарий')
        self.lineEdit_comment.setGeometry(450, 710, 450, 60)

        self.lbllevel = QLabel("Уровень важности", self)
        self.lbllevel.setFont(self.font_lbl)
        self.lbllevel.setGeometry(1080, 30, 300, 65)
        # рисуем точки выбора уровней важности
        self.radiobtn_lowlvl = QRadioButton('Низкий', self)
        self.radiobtn_lowlvl.setChecked(True)
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

        self.lbllevel = QLabel("Дата устранения", self)
        self.lbllevel.setFont(self.font_lbl)
        self.lbllevel.setGeometry(50, 570, 200, 65)

        current_date = datetime.now()
        self.edit_solve_date = QDateEdit(self)
        self.edit_solve_date.setGeometry(50, 630, 200, 80)
        self.edit_solve_date.setFont(self.font_lbl)
        # d = (current_time.strftime('%m/%d/%Y'))
        self.edit_solve_date.setDate(current_date)

        self.btn_save.setStyleSheet(qss_file)
        self.btn_close.setStyleSheet(qss_file)

    def hide_second_window(self):  # кнопка закрыть форму на дочерней форме
        # self.check_visibility() #проверяем главное окно на отображение и показываем
        self.hide()  # закрываем текущую форму
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_data(self):
        dict_of_params = read_data_txt()  # функция из модуля database
        for keys, values in dict_of_params.items():
            # print(keys, values)
            if keys == 'список несоответствий':
                self.qlistw_defects.addItems(values)
                break
        if keys != 'список несоответствий':
            QMessageBox.critical(self, 'Данные не загружены!', 'Отсутствует файл "список несоответствий.txt"')

    def click_save_results(self):
        defect = self.qlistw_defects.currentItem()  # несоответсвие
        defect_grade = self.cbox_defect_grade.currentText()  # бальная оценка несоотвествия
        cons_grade = self.cbox_consequences_grade.currentText()  # бальная оценка последствий
        detection_type = self.find_checked_rbtn_inspect()  # типа обнаружения
        importance_lvl = self.find_checked_rbtn_lvl()  # уровень важности
        comment = self.lineEdit_comment.text()  # комментарий
        solve_date = self.edit_solve_date.text()  # дата устранения

        self.btn_close.setEnabled(True)  # делаем форму закрытия активной после записи данных

        if defect and detection_type is not None:
            # db_delete()  # функция из database.py
            # db_connect()  # функция из database.py
            # добавляем данные в БД из таблицы несоотвествий в последнюю запись в БД.
            db_insert_defects(defect.text(), defect_grade, cons_grade, detection_type,
                              importance_lvl, comment, solve_date)  # функция из database.py
            table_results = db_select()  # функция из database.py для для проверки
            self.hide_second_window()  # функция в этом классе

            # выводим в консоль для проверки
            for row in table_results:
                print('\nНаша таблица с добавлением results БД db_results.db\n', row)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Не все параметры выбраны!')

    # функция возвращает имя выбранного элементы осмотра radiobutton
    def find_checked_rbtn_inspect(self):
        # перебираем наши radiobuttons в groupbox и получаем их порядковые номера
        checklist = ([i for i, button in enumerate(self.grbox_rbtninspect.buttons()) if button.isChecked()])
        if checklist is not None:
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


# def closeEvent(self, event):
# reply = QMessageBox.question(self, 'Закрытие формы',
#          "Уверены? Все незаписанные данные текущей формы будут потеряны", QMessageBox.Yes |
#   QMessageBox.No, QMessageBox.No)
# if reply == QMessageBox.Yes:
#  event.accept()
#  else:
# event.ignore()


# класс для обработки ошибок, управление потоком
class MadeToFail(QThread):
    error_ocurred = pyqtSignal(Exception, name="errorOcurred")

    # тест
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
