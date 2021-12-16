import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QApplication, QPushButton, QMessageBox, QDialog, \
    QComboBox
from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from database import read_data_txt
from ui import *


class LoginForm(QWidget):
    #    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(LoginForm, self).__init__()

        self.setWindowTitle('Окно входа')
        self.resize(500, 120)
        self.setFixedSize(500,120)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        layout = QGridLayout()
        label_name = QLabel('<font size ="4"> Логин: </font>')
        # self.lineEdit_username = QLineEdit()
        # self.lineEdit_username.setPlaceholderText('Введите имя для входа')
        self.cbox_oper = QComboBox()
        layout.addWidget(self.cbox_oper, 0, 1)
        layout.addWidget(label_name, 0, 0)
        # layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size ="4"> Пароль: </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Введите пароль')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        btn_login = QPushButton('Войти')
        btn_login.clicked.connect(self.login_check)
        layout.addWidget(btn_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

        data = read_data_txt()  # функция из модуля database
        for key, value in data.items():
            if key == 'список операторов':
                self.cbox_oper.addItems(value)
                print('Проверка функции add_operators-', value)
                break
        if key != 'список операторов':
            QMessageBox.critical(self, 'Ошибка чтения данных', 'Отсутствует файл "список операторов.txt"')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Выйти из программы?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            exit()
        else:
            event.ignore()

    def login_check(self):
        msg = QMessageBox()
        if self.lineEdit_password.text() == '123':
            # пока на скорую руку через файл, потом сделаем через БД
            with open('current_operator.txt', 'w') as file:
                file.write(self.cbox_oper.currentText())
            msg.setText('Упешно')
            msg.exec_()
            self.close()
        else:
            msg.setText('Неверные данные')
            msg.exec_()

    def login(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = LoginForm()
        # self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        pass
        # self.window = MainWindow()
        # self.window.switch_window.connect(self.show_window_two)
        # self.login.close()
        # self.window.show()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
