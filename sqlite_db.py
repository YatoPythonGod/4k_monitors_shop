from os import path
import sqlite3
from datetime import date

sqlite_connection = False


async def create_db(sql_script_file='create_table.sql') -> None:
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(f'4k_monitors_shop_{date.today()}.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        with open(sql_script_file, encoding='utf-8') as sqlite_file:
            sql_script = sqlite_file.read()
        cursor.executescript(sql_script)
        sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def checking_dv_today():
    return True if path.exists(f'{path.dirname(__file__)}\\4k_monitors_shop_{date.today()}.db') else False


def insert_varible_into_table(data_tuple):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(f'4k_monitors_shop_{date.today()}.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO monitors
                              ("Полное наименование", "Диагональ", "Соотношение сторон", "Максимальное разрешение", 
                              "Тип матрицы", "Максимальная частота обновления (FPS, Гц)", "Цена", "Бренд", "Ссылка")
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        for i, el in enumerate(data_tuple, start=1):
            cursor.execute(sqlite_insert_with_param, tuple(el.values()))
        #    await bot.send_message(message.chat.id, f'Страница {i} загруженна! Осталось: {58 - i}') # !!!
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу monitors")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def get_db_data(row_size, row_id, filters):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(f'4k_monitors_shop_{date.today()}.db')
        sqlite_connection.row_factory = sqlite3.Row
        cursor = sqlite_connection.cursor()

        sql_select = []
        for k, v in filters.items():
            if k in ['Цена', 'Диагональ', 'Частота кадров']:
                if k == 'Частота кадров':
                    sql_select.append(f'("Максимальная частота обновления (FPS, Гц)" BETWEEN {v[0]} AND {v[1]})')
                else:
                    sql_select.append(f'({k} BETWEEN {v[0]} AND {v[1]})')
            elif k in ['Тип матрицы', 'Разрешение', 'Бренд']:
                if k == 'Разрешение':
                    k = '"Максимальное разрешение"'
                    res_str = f" OR {k}=".join(list(map(lambda x: f'"{x}"', v)))
                    sql_select.append(f'({k}={res_str})')
                else:
                    k = f'"{k}"'
                    res_str = f" OR {k}=".join(list(map(lambda x: f'"{x}"', v)))
                    sql_select.append(f'({k}={res_str})')

        sqlite_select_query = f'SELECT rowid, * from monitors WHERE rowid>{row_id} AND Цена>0 AND {" AND ".join(sql_select)} ORDER BY Цена'
        print(sqlite_select_query)
        cursor.execute(sqlite_select_query)
        result = [dict(row) for row in cursor.fetchmany(row_size)]
        cursor.close()
        if sqlite_connection:
            sqlite_connection.close()
        return result

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def get_criteria():
    global sqlite_connection
    try:
        if checking_dv_today():
            sqlite_connection = sqlite3.connect(f'4k_monitors_shop_{date.today()}.db')
            cursor = sqlite_connection.cursor()
            sqlite_select_query = """SELECT * from monitors"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()

            brand = set()
            diagonal = set()
            resolution = set()
            matrix = set()
            frequency = set()
            price = set()

            for row in records:
                brand.add(row[7])
                diagonal.add(row[1])
                resolution.add(row[3])
                if row[4] != '-':
                    matrix.add(row[4])
                if row[5] != 0:
                    frequency.add(row[5])
                if row[6] != 0:
                    price.add(row[6])
            print(price)
            cursor.close()
            criteria_dict = {'Цена': [min(price), max(price)],
                             'Бренд': brand,
                             'Диагональ': [min(diagonal), max(diagonal)],
                             'Разрешение': list(sorted(resolution, key=lambda x: (x.split('×')[0]))),
                             'Тип матрицы': matrix,
                             'Частота кадров': [min(frequency), max(frequency)]}
            return criteria_dict
        else:
            return
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
