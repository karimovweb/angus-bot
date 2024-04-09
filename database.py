import sqlite3
from datetime import datetime

connection = sqlite3.connect("baza_dannix.db")
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, work TEXT,'
            'phone_number TEXT, language TEXT, reg_date DATETIME);')
sql.execute('CREATE TABLE IF NOT EXISTS work (user_id INTEGER, rayon1 TEXT, rayon2 TEXT,'
            'rayon3 TEXT, rayon4 TEXT);')


def add_user(user_id, user_name, user_work, user_phone_number, language):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    sql.execute('INSERT INTO users (user_id, name, work, phone_number, language, reg_date) VALUES (?, ?, ?, ?, ?, ?);',
                (user_id, user_name, user_work, user_phone_number, language, datetime.now()))
    connection.commit()


def get_users():
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    users = sql.execute('SELECT * FROM users;').fetchall()
    return users

def check_users(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    checker = sql.execute('SELECT user_id FROM users WHERE user_id = ?;', (user_id,)).fetchone()
    if checker:
        return True
    else:
        return False
def check_id(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    checker = sql.execute('SELECT user_id FROM users WHERE user_id = ?;', (user_id,)).fetchone()
    return checker


def check_language(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT language FROM users WHERE user_id = ?;", (user_id,))
    if checker.fetchone() == ("Uzb",):
        return "uzb"
    elif checker.fetchone() == ("Rus",):
        return "rus"
    return False


def work(user_id, rayon1='Район 1', rayon2='Район 2', rayon3='Район 3', rayon4='Район 4'):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO work (user_id, rayon1, rayon2, rayon3, rayon4) VALUES (?, ?, ?, ?);", (user_id, rayon1,
                                                                                                    rayon2, rayon3,
                                                                                                    rayon4))
    connection.commit()


def from_work(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    sql.execute('SELECT * FROM work WHERE user_id = ?;', (user_id,))
    result = sql.fetchone()
    return result


def get_user_name(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    sql.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    name = sql.fetchone()
    if name:
        return name[0]  # Возвращаем первый элемент кортежа (имя)
    else:
        return None


def get_location(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    sql.execute('SELECT work FROM users WHERE user_id = ?;', (user_id,))
    result = sql.fetchone()
    return result


def get_number(user_id):
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    sql.execute('SELECT phone_number FROM users WHERE user_id = ?', (user_id,))
    result = sql.fetchone()
    if result:
        return result[0]
    else:
        return None

def mailing_all():
    connection = sqlite3.connect("baza_dannix.db")
    sql = connection.cursor()
    all_targets = sql.execute("SELECT user_id FROM users;",).fetchall()
    return all_targets