import sqlite3

connection = sqlite3.connect('Solved_HW.db')
cursor = connection.cursor()


def check_presence(number, cycle, fluid, p2_1, p2_2, p1, Tx, Tcond, Tev):
    cursor.execute(f"SELECT * FROM Users WHERE number = {number} AND fluid = '{fluid}' AND cycle = '{cycle}'"
                   f"AND p2_1 = {p2_1} AND p2_2 = {p2_2} AND p1 = {p1} AND Tx = {Tx} AND Tcond = {Tcond} AND "
                   f"Tev = {Tev} ON CONFLICT (number, cycle, fluid, p2_1, p2_2, p1, Tx, Tcond, Tev) DO NOTHING")
    user = cursor.fetchone()
    if user is not None:
        return True
    else:
        return False


def add_solved_task(number, surname, cycle, fluid, p2_1, p2_2, p1, Tx, Tcond, Tev):
    cursor.execute('INSERT INTO Users (number, surname, cycle, fluid, p2_1, p2_2, p1, Tx, Tcond, Tev) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (number, surname, cycle, fluid, p2_1,
                                                             p2_2, p1, Tx, Tcond, Tev))
    connection.commit()
    print('База данных обновлена')


def count_users():
    cursor.execute('SELECT COUNT(*) FROM Users')
    total_users = cursor.fetchone()[0]
    print('Общее количество пользователей:', total_users)


db_actions = {'Добавить решённую задачу': add_solved_task,
              'Подсчитать кол-во решённых задач': count_users}

if __name__ == '__main__':
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    number INTEGER NOT NULL,
    surname TEXT NOT NULL,
    cycle TEXT NOT NULL,
    fluid TEXT NOT NULL,
    p2_1 INTEGER,
    p2_2 INTEGER,
    p1 REAL,
    Tx INTEGER,
    Tcond INTEGER,
    Tev INTEGER
    )
    ''')
    # action = input(f'Выберите действие из списка: {list(db_actions.keys())}\n'
    #                f'Введите действие (для завершения оставьте поле пустым): ')
    # while action != '':
    #     try:
    #         db_actions[action]()
    #         action = input(f'Выберите действие из списка: {list(db_actions.keys())}\n'
    #                        f'Введите действие (для завершения оставьте поле пустым): ')
    #     except KeyError:
    #         print('Видимо вы ввели что-то не так, попробуйте ещё раз')
    #         action = input(f'Выберите действие из списка: {list(db_actions.keys())}\n'
    #                        f'Введите действие (для завершения оставьте поле пустым): ')
    #     except TypeError:
    #         print('Данное действие не предусмотрено')
    connection.commit()
    connection.close()

