"""Модуль отвечает за атворизацию пользователей по имени и паролю"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QApplication, QPushButton, QMessageBox, QDialog, \
    QComboBox
from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from database import read_data_txt
from main import *


class LoginForm(QWidget):
    #    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(LoginForm, self).__init__()
        qss_file = open('style_file.css').read()
        self.setWindowTitle('Окно авторизации')
        self.resize(500, 120)
        self.setFixedSize(500, 120)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.font_lbl = QFont()
        self.font_lbl.setPointSize(12)
        self.font_lbl.setBold(True)
        self.font_lbl.setWeight(75)

        self.font_cbox = QFont()
        self.font_cbox.setPointSize(16)
        self.font_cbox.setBold(True)
        self.font_cbox.setWeight(80)

        layout = QGridLayout()
        label_name = QLabel('<font size ="4"> Имя: </font>')
        # self.lineEdit_username = QLineEdit()
        # self.lineEdit_username.setPlaceholderText('Введите имя для входа')
        self.cbox_oper = QComboBox()
        self.cbox_oper.setFont(self.font_cbox)
        layout.addWidget(self.cbox_oper, 0, 1)
        layout.addWidget(label_name, 0, 0)
        # layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size ="4"> Пароль: </font>')
        self.lineEdit_password = QLineEdit()
        # self.lineEdit_password.setPlaceholderText('Введите пароль')
        self.lineEdit_password.setFont(self.font_cbox)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        btn_login = QPushButton('Войти')
        btn_login.clicked.connect(self.login_check)
        btn_login.setFont(self.font_lbl)
        layout.addWidget(btn_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

        data = read_data_txt()  # функция из модуля database
        for key, value in data.items():
            if key == 'список операторов':
                self.cbox_oper.addItems(value)
                # print('Проверка функции add_operators-', value)
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
        date = datetime.today()
        current_date = str((date.strftime('%d.%m.%Y %H:%M')))

        msg = QMessageBox()
        if self.lineEdit_password.text() == 'Age12345':
            # пока на скорую руку через файл, потом можно сделать через БД
            with open('temp/buffer_operator.txt', 'w') as file:
                file.write(self.cbox_oper.currentText())
            with open('temp/logs.txt', 'a') as file:
                file.write(current_date + ' вход в систему: ' + self.cbox_oper.currentText() + '\n')

            msg.setText('Вы успешно вошли в программу')
            msg.exec_()
            self.hide()
        else:
            msg.setText('Неверный пароль!')
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
