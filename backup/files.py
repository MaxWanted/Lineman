"""
В модуле объявлены функции работающие с чтением файлов и передающие результаты
в модуль main.py
"""

import os
import sqlite3
from main import *



# функция читает все .txt файлы в корне для работы и загружает их имена в словарь как ключи и данные как значения
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




# функция читает список операторов из файла
# def read_operators():
# with open('список операторов.txt', "r") as file:
# lines = file.read().split("\n")
# file.close()
# return lines


# функция загрузки списка объектов из файла, где ключ название файла-объекта, а значенияя это параметры проверки внутри
# def read_objects():
# with open('список объектов.txt', 'r') as file:
# lines = file.read().split("\n")
# file.close()
# return lines
