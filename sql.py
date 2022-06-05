import sqlite3
import toml


class Sql:
    def __init__(self):
        self.CFG = toml.load("config.toml")
        self.DATABASE_NAME = self.CFG["database"]

    @property
    def connection(self):
        return sqlite3.connect(self.DATABASE_NAME)

    @property
    def cursor(self):
        return self.connection.cursor()

