import sys, os, os.path
from PyQt5.QtCore import QDate, Qt, QDateTime, QTime, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QToolTip, QPushButton, QComboBox, QLabel, \
    QDesktopWidget
from files import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(200, 200, 1150, 768)
        self.setWindowTitle("Арм Обходчик")

        now = QDate.currentDate()
        time = QTime.currentTime()

        # определяем стиль шрифта для надписей и кнопок
        font_lbl = QFont()
        font_lbl.setPointSize(12)
        font_lbl.setBold(True)
        font_lbl.setWeight(75)

        # определяем шрифт для всех комбобоксов
        font_cbox = QFont()
        font_cbox.setPointSize(16)
        font_cbox.setBold(True)
        font_cbox.setWeight(75)

        # setGeometry(10, 100, 150, 30)   (отступ от левого края, ширина, отступ сверху, высота)

        # надпись дата
        lbl_date = QLabel("Дата", self)
        lbl_date.setText(now.toString(Qt.ISODate))
        lbl_date.setGeometry(10, 100, 150, 30)
        lbl_date.setFont(font_lbl)

        # надпись время
        lbl_time = QLabel("Время", self)
        lbl_time.setText(time.toString(Qt.DefaultLocaleLongDate))
        lbl_time.setGeometry(150, 100, 150, 30)
        lbl_time.setFont(font_lbl)

        # надпись смена
        lbl_shift = QLabel("Дневная смена", self)
        lbl_shift.setGeometry(250, 100, 200, 30)
        lbl_shift.setFont(font_lbl)

        # надпись информация
        lbl_info = QLabel("Информация", self)
        lbl_info.setGeometry(450, 100, 510, 30)
        lbl_info.setFont(font_lbl)

        # надпись параметр проверки
        lbl_parameter = QLabel(self)
        lbl_parameter.setText("Это текстово поле для параметров проверки оборудования")
        lbl_parameter.setGeometry(10, 300, 700, 300)
        lbl_parameter.setFont(font_lbl)

        # список выбора оператора
        self.cbox_operator = QComboBox(self)
        self.cbox_operator.setGeometry(QRect(10, 150, 400, 50))
        self.cbox_operator.setFont(font_cbox)

        # список выбора объекта проверки
        self.cbox_object = QComboBox(self)
        self.cbox_object.setGeometry(QRect(450, 150, 400, 50))
        self.cbox_object.setFont(font_cbox)

        # кнопка загрузки списка операторов из текстового файла
        btn_addoperators = QPushButton("Загрузить список операторов", self)
        btn_addoperators.setGeometry(10, 5, 200, 40)
        btn_addoperators.clicked.connect(self.click_add_operators)

        # кнопка загрузки списка объектов проверки из текстового файла
        self.btn_addobjects = QPushButton("Загрузить список объектов", self)
        self.btn_addobjects.setGeometry(230, 5, 200, 40)
        self.btn_addobjects.clicked.connect(self.click_add_objects)

        # кнопка пролистывания списка вперед
        self.btn_next = QPushButton("Следующий", self)
        self.btn_next.setGeometry(900, 300, 200, 50)
        self.btn_next.setFont(font_lbl)
        self.btn_next.clicked.connect(self.get_objects)

        # кнопка пролистывания списка назад
        btn_prev = QPushButton("Предыдущий", self)
        btn_prev.setGeometry(900, 375, 200, 50)
        btn_prev.setFont(font_lbl)
        # self.btn_prev.clicked.connect(self.do_next)

        # кнопка подтвержедния выбора оператора и объекта проверки
        self.btn_confirm = QPushButton("Подтвердить выбор", self)
        self.btn_confirm.setGeometry(900, 150, 200, 50)
        self.btn_confirm.setFont(font_lbl)
        # используем lambda фукнцию т.к. она необходима для передач параметров
        self.btn_confirm.clicked.connect(self.click_add_params)

        btn_exit = QPushButton("Выход", self)
        btn_exit.clicked.connect(QApplication.instance().quit)
        btn_exit.setFont(font_lbl)
        btn_exit.setGeometry(900, 600, 200, 50)

        msg = QMessageBox()
        msg.setWindowTitle("Название окна")
        msg.setText("Описание")
        msg.setIcon(QMessageBox.Warning)

        # self.statusBar().showMessage('Ready')
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # диалоговое окно выхода
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # далее идет блок функций обрабатывающий нажатие кнопок на форме

    def click_add_operators(self):
        data = read_operators()  # функция из модуля files
        self.cbox_operator.clear()
        self.cbox_operator.addItems(data)
        print(data)

    def click_add_objects(self):
        data = read_objects()  # функция из модуля files
        self.cbox_object.clear()
        self.cbox_object.addItems(data)
        print(data)

    def click_add_params(self):
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

    # фкнкция из files выводит словарь, где ключ название файла-объекта, а значенияя это параметры проверки внутри
    def get_objects(self):
        dict_of_params = read_data_txt()
        for keys, values in dict_of_params.items():
            print(keys, values)


def main():
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
