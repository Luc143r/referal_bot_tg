from sqlite3 import connect, Cursor


def db_session(method):
    def wrapper(self, *args, **kwargs):
        connection = connect('data/data.db')
        cursor = connection.cursor()
        try:
            return method(self, *args, **kwargs, cursor=cursor)
        finally:
            connection.commit()
            connection.close()
    return wrapper


class Database:
    @db_session
    def __init__(self, cursor: Cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            user TEXT NOT NULL UNIQUE,
            link TEXT NOT NULL UNIQUE,
            balance INTEGER,
            ref_balance INTEGER,
            all_ref INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            owner_id INTEGER,
            date TEXT
        )
        ''')

    @db_session
    def insert_partner(self, user_id: int, username: str, link: str, cursor: Cursor):
        cursor.execute(
            'INSERT INTO Partners (user_id, user, link, balance, ref_balance, all_ref) VALUES (?, ?, ?, ?, ?, ?)', (user_id, username, link, 0, 0, 0))

    @db_session
    def insert_user(self, user_id: int, owner_id: str, date: str, cursor: Cursor):
        cursor.execute(
            'INSERT INTO Users (user_id, owner_id, date) VALUES (?, ?, ?)', (user_id, owner_id, date))

    @db_session
    def select_partner(self, user_id: int, cursor: Cursor):
        cursor.execute(
            'SELECT * FROM Partners WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def get_partner(self, link: str, cursor: Cursor):
        cursor.execute(
            'SELECT user_id FROM Partners WHERE link = ?', (link,))
        result = cursor.fetchone()
        return result

    @db_session
    def select_link(self, user_id: int, cursor: Cursor):
        cursor.execute(
            'SELECT link FROM Partners WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def select_user(self, user_id: int, cursor: Cursor):
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def select_balance(self, user_id: int, cursor: Cursor):
        cursor.execute(
            'SELECT balance FROM Partners WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def select_ref_balance(self, user_id: int, cursor: Cursor):
        cursor.execute(
            'SELECT ref_balance FROM Partners WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def select_all_ref(self, user_id: int, cursor: Cursor):
        cursor.execute(
            'SELECT all_ref FROM Partners WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result

    @db_session
    def select_user_on_date(self, owner_id: int, date: str, cursor: Cursor):
        cursor.execute(
            'SELECT * FROM Users WHERE owner_id = ? AND date = ?', (owner_id, date,))
        result = cursor.fetchall()
        return len(result)

    @db_session
    def update_ref_balance(self, user_id: int, count: int, cursor: Cursor):
        cursor.execute(
            'UPDATE Partners SET ref_balance = ? WHERE user_id = ?', (count, user_id,))

    @db_session
    def update_all_ref(self, user_id: int, count: int, cursor: Cursor):
        cursor.execute(
            'UPDATE Partners SET all_ref = ? WHERE user_id = ?', (count, user_id,))
