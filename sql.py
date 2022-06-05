import sqlite3
from typing import Tuple, List
from support import request_header
import toml


rows = Tuple[str, str, str, str, str, str]


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
        return self.connection.cursor

    def select(self, table, column_list='*'):
        self.request = f"SELECT {column_list} FROM {table}"
        return self

    def where(self, *args, **kwargs):
        self.request += " WHERE "
        self.request += (" and ".join(f'{k} = \"{v}\"' for k, v in kwargs.items()))
        return self

    def execute(self, *value: rows):
        if value:
            self.request += " VALUES "
            self.request += str(value)
        self.cursor().execute(self.request)
        self.connection.commit()
        return self

    def executemany(self, values: List[rows]):
        for value in values:
            self.cursor().execute(self.request, value)
            self.connection.commit()
        return self

    def insert(self, table: str):
        self.request = f"INSERT INTO '{table}' {request_header(table)}"
        return self

    def update(self, table: str):
        self.request = f"UPDATE {table}"
        return self

    def set(self, *args, **kwargs):
        def text(items):
            return ", ".join(f"{k} = \'{v}\'" for k, v in items)

        self.request += " SET "

        if args:
            self.request += text(zip(*args))
        if kwargs:
            self.request += text(kwargs.items())
        return self

    def commit(self):
        self.request = str()
