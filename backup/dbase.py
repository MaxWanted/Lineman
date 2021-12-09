import sqlite3


def connect():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE  IF NOT EXISTS results (
                date TEXT,
                time TEXT,
                shift TEXT,
                operator TEXT,
                object TEXT,
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


"""
def insert():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO results VALUES ('01.01.2021', '20:55', 'Дневная смена', 'Иванов Иван Иванович', "
                   "'Трансформатор 1', 'Соответствие состояния коммутационных аппаратов, контактной группы, соответствие их\
               положений схеме режима работы, соответствие состояния приводов', 'Да', 'Коррозионный износ', 'Средний', "
                   "'Средний', '25.12.2020', '27.12.2020','Комментарий','50','40','Петров Петр Петрович')")

    connection.commit()
    connection.close()
"""


def select():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM results")
    print(cursor.fetchall())
    connection.commit()
    connection.close()
