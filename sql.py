import sqlite3
import toml


class Sql:
    def __init__(self):
        self.CFG = toml.load("config.toml")
        self.DATABASE_NAME = self.CFG["database"]
        self.request = str()

    @property
    def connection(self):
        return sqlite3.connect(self.DATABASE_NAME)

    @property
    def cursor(self):
        return self.connection.cursor()

    def select(self, table, column_list='*'):
        self.request = f"SELECT {column_list} FROM {table}"
        return self

    def where(self, *args, **kwargs):
        self.request += " WHERE "
        self.request += (" and ".join(f'{k} = \"{v}\"' for k, v in kwargs.items()))
        return self

    def execute(self):
        return self.cursor.execute(self.request)

    def executemany(self, rows):
        self.cursor.executemany(self.request, rows)
        return self

    def insert(self, table: str):
        self.request = f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)"
        return self

    def table(self, table: str):
        self.request.replace("%table%", table)
        return self

    def commit(self):
        self.connection.commit()
        self.request = str()
