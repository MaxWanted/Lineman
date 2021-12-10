"""Модуль работы с базой данных sqlite3 и текстовыми файлами"""
import os
import sqlite3
from datetime import datetime

from PyQt5.QtWidgets import QWidget

from ui import MainWindow


# создание  БД с таблицей
def db_connect():
    connection = sqlite3.connect('db_results.db')
    cursor = connection.cursor()

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
    connection.close()


# вставка данных в таблицу
def db_insert(item, obj, oper, shift):
    # все статичные данные для таблицы
    current_date = str(datetime.now().date())
    date = datetime.today()
    current_time = str((date.strftime('%H:%M')))

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
                   (current_date, current_time, shift, oper, obj, item, '', '', '', '', '', '', '', '', '', ''))

    connection.commit()
    connection.close()


# выборка из БД
def db_select():
    connection = sqlite3.connect('db_results.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM results")
    # print (cursor.fetchall())
    return cursor.fetchall()
    connection.close()


# удаление из бД
def db_delete():
    connection = sqlite3.connect('db_results.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM results")
    connection.commit()
    connection.close()


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
