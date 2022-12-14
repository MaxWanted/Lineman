"""Модуль работы с базой данных sqlite3 и текстовыми файлами"""

import os
import sqlite3
from datetime import datetime

from PyQt5.QtWidgets import QWidget


# создание  БД с таблицей
def db_connect():
    date = datetime.today()
    current_date = str((date.strftime('%d.%m.%Y %H:%M')))
    try:
        connection = sqlite3.connect('db_results.db')
        cursor = connection.cursor()

        # log_db("база данных создана и успешно подключена к SQLite")  # фукнция заиси логов

        cursor.execute("""CREATE TABLE  IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    time TEXT,
                    shift TEXT,
                    operator TEXT,
                    object_check TEXT,
                    parameter TEXT,
                    checkout TEXT,
                    defect TEXT,
                    importance_lvl TEXT,
                    detection_type TEXT,
                    detection_date TEXT,
                    solve_date TEXT,
                    comment TEXT,
                    grade INTEGER,
                    defect_grade INTEGER,
                    who_knows TEXT                                
                )""")

        connection.commit()
        # log_db('таблица БД успешно создана')
        connection.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        log_db(error)


# вставка данных в таблицу
def db_insert(item, obj, oper, shift, checkout):
    # все статичные данные для таблицы
    # current_date = str(datetime.now().date())
    date = datetime.today()
    current_date = str(date.strftime('%d.%m.%Y'))
    current_time = str((date.strftime('%H:%M')))

    try:
        connection = sqlite3.connect('db_results.db')
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO results (
                        date,
                        time,
                        shift,
                        operator,
                        object_check,
                        parameter,
                        checkout,
                        defect,
                        importance_lvl,
                        detection_type,
                        detection_date,
                        solve_date,
                        comment,
                        grade,
                        defect_grade,
                        who_knows
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                       (current_date, current_time, shift, oper, obj, item, checkout, '', '', '', '', '', '', '', '',
                        ''))

        connection.commit()
        # log_db('данные положительной проверки успешно записаны в базу данных ')
        connection.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        log_db(error)


# вставка(обновление) данных из второй формы в таблицу
def db_insert_defects(defect, grade, cons_grade, detection_type, importance_lvl, comment, solve_date):
    # все статичные данные для таблицы
    date = datetime.today()
    current_date = str(date.strftime('%d.%m.%Y'))  # форматируем дату в российский формат

    try:
        connection = sqlite3.connect('db_results.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE results SET defect=?, importance_lvl=?, detection_type=?, grade=?, "
                       "defect_grade=?, detection_date=?, solve_date=?, comment=? "
                       "WHERE ID = (SELECT MAX(ID) from results)",
                       (defect, importance_lvl, detection_type, cons_grade, grade, current_date, solve_date,
                        comment))

        connection.commit()
        # log_db('данные проверки несоответствий успешно записаны в базу данных ')
        connection.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        log_db(error)


# выборка из БД для проверки
def db_select():
    connection = sqlite3.connect('db_results.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM results")
    # print (cursor.fetchall())
    return cursor.fetchall()
    connection.close()


# удаление из бД  если необходимо
def db_delete():
    connection = sqlite3.connect('db_results.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM results")
    connection.commit()
    connection.close()


# функция логирования
def log_db(msg):
    date = datetime.today()
    current_date = str((date.strftime('%d.%m.%Y %H:%M')))
    with open('temp/logs.txt', 'a') as file:
        file.write(current_date + ' ' + msg + '\n')


# отдельные функции чтения txt файлов
def read_data_txt():
    files = os.listdir()
    objects_txt = []
    for file in files:
        if file.endswith('.txt'):  # читаем только файлв с расширением txt в корне
            objects_txt.append(file)

    dict_of_params = dict()

    for file in objects_txt:
        with open(file, 'r') as f:
            word_list = f.read().split("\n")  # избавляемся от знака переноса
            word_list[:] = [item for item in word_list if item != '']  # удаляем пустые строки из списка
            # удаляем расширение txt и добавляем в словарь, имя файла ключ - строки внутри  значения
            dict_of_params[str(f.name.rsplit(".", 1)[0])] = word_list
        f.close()
    return dict_of_params
