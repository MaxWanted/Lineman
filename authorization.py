import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QApplication, QPushButton, QMessageBox, QDialog
from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from ui import MainWindow


class LoginForm(QWidget):
#    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(LoginForm, self).__init__()

        self.setWindowTitle('Окно входа')
        self.resize(500, 120)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        layout = QGridLayout()
        label_name = QLabel('<font size ="4"> Логин: </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Введите имя для входа')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

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

    def login_check(self):
        msg = QMessageBox()

        if self.lineEdit_username.text() == '123' and self.lineEdit_password.text() == '123':
            msg.setText('Упешно')
            msg.exec_()



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
        #self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.window = MainWindow()
        # self.window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    # def show_window_two(self, text):
    # self.window_two = WindowTwo(text)
    # self.window.close()
    # self.window_two.show()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()