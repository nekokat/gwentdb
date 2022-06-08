import sqlite3
from typing import Tuple, List
import toml

rows = Tuple[str, str, str, str, str, str]

MASTER_TABLE = ("lastrow", "games")
PIVOT_TABLE = ("win_loss", "versus", "overall")


# config
cfg = toml.load("config.toml")
FRACTIONS = dict(cfg["fraction"])
RESULT = dict(cfg["result"])


def request_header(table: str) -> tuple:
    """Creating a tuple for a database query"""
    main_title = ("game_mode", "fraction", "opponent", "opponent_fraction", "result", "score",)
    header = RESULT if table == "win_loss" else FRACTIONS
    columns = tuple(header.values())
    table_header = None
    if table in ("win_loss", "versus"):
        table_header = ("Fraction",) + columns
    elif table == "overall":
        table_header = ("Overall",) + columns
    elif table in ("games", "lastrow"):
        table_header = main_title
    return table_header


def and_(**kwargs) -> str:
    return " and ".join(f"{k} = \'{v}\'" for k, v in kwargs.items())


def or_(**kwargs) -> str:
    return " or ".join(f"{k} = \'{v}\'" for k, v in kwargs.items())


def _table_header(table: str) -> str:
    """Creating table header for db query"""
    header = request_header(table)
    length = len(header)
    col_types = None
    if table in ("lastrow", "games"):
        col_types = ("TEXT",) * length
    elif table in ("win_loss", "versus"):
        col_types = ("TEXT",) + ("INTEGER",) * (length - 1)
    elif table == "overall":
        col_types = ("INTEGER",) * length
    title = [f'"{col}" {col_type}' for col, col_type in zip(header, col_types)]
    return "({})".format(", ".join(title))


class Query:
    def __init__(self):
        self.CFG = toml.load("config.toml")
        self.DATABASE_NAME = self.CFG["database"]
        self.request = str()
        self.connection = sqlite3.connect(self.DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def select(self, table, column_list='*'):
        self.request = f"SELECT {column_list} FROM {table}"
        return self

    def create(self, table: str):
        """Database query to create a table"""
        self.request += f"CREATE TABLE {table} {_table_header(table)}"
        return self

    def where(self, *args, **kwargs):
        if not args and not kwargs:
            return self
        self.request += " WHERE "
        if args:
            self.request += args
        if kwargs:
            self.request += and_(**kwargs)
        return self

    def fetchall(self):
        fetch = self.cursor.execute(self.request).fetchall()
        self.commit()
        return fetch

    def drop(self, table: str):
        self.request += f"DROP TABLE {table}"
        return self

    def execute(self, *value: rows):
        if value:
            self.request += " VALUES "
            self.request += str(*value)
        self.cursor.execute(self.request)
        return self

    def executemany(self, values: List[rows]):
        req = self.request[:]
        for value in values:
            self.request = req
            self.execute(value).commit()
        return self

    def insert(self, table: str):
        self.request += f"INSERT INTO '{table}' {request_header(table)}"
        return self

    def update(self, table: str):
        self.request += f"UPDATE {table}"
        return self

    def set(self, *args, **kwargs):
        if not args and not kwargs:
            return self

        def text(items):
            return ", ".join(f"{k} = \'{v}\'" for k, v in items)

        self.request += " SET "
        if args:
            self.request += text(zip(*args))
        if kwargs:
            self.request += text(kwargs.items())
        return self

    def commit(self):
        self.connection.commit()
        self.request = str()
        return self
