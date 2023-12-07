import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data/data.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL UNIQUE,
            link TEXT NOT NULL UNIQUE,
            balance INTEGER,
            ref_balance INTEGER,
            all_ref INTEGER
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL UNIQUE,
            owner TEXT,
            date TEXT
        )
        ''')
        self.connection.commit()

    def insert_partner(self, username: str, link: str):
        self.cursor.execute(
            'INSERT INTO Partners (user, link, balance, ref_balance, all_ref) VALUES (?, ?, ?, ?, ?)', (username, link, 0, 0, 0))
        self.connection.commit()

    def insert_user(self, username: str, owner: str, date: str):
        self.cursor.execute(
            'INSERT INTO Users (user, owner, date) VALUES (?, ?, ?)', (username, owner, date))
        self.connection.commit()

    def select_partner(self, username: str):
        self.cursor.execute(
            'SELECT * FROM Partners WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def get_partner(self, link: str):
        self.cursor.execute('SELECT user FROM Partners WHERE link = ?', (link,))
        result = self.cursor.fetchone()
        return result

    def select_link(self, username: str):
        self.cursor.execute('SELECT link FROM Partners WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def select_user(self, username: str):
        self.cursor.execute('SELECT * FROM Users WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def select_balance(self, username: str):
        self.cursor.execute(
            'SELECT balance FROM Partners WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def select_ref_balance(self, username: str):
        self.cursor.execute(
            'SELECT ref_balance FROM Partners WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def select_all_ref(self, username: str):
        self.cursor.execute(
            'SELECT all_ref FROM Partners WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def update_ref_balance(self, username: str, count: int):
        self.cursor.execute(
            'UPDATE Partners SET ref_balance = ? WHERE user = ?', (count, username,))
        self.connection.commit()

    def update_all_ref(self, username: str, count: int):
        self.cursor.execute(
            'UPDATE Partners SET all_ref = ? WHERE user = ?', (count, username,))
        self.connection.commit()

    def _close_connection(self):
        self.connection.close()
