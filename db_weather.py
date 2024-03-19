import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("weather_app.db")
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY,
                username TEXT,
                query TEXT,
                result TEXT,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        """
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
