from support import wheretostr, request_header, settostr
from connection import CONN, CURSOR
from typing import Union

# table title
games_title = (
    "game_mode",
    "fraction",
    "opponent",
    "opponent_fraction",
    "result",
    "score",
)


def count(table: str, _where: list = []) -> int:
    """Counts the number of rows for a given condition"""
    _where = f" WHERE {wheretostr(_where, ' AND ')}" if _where != [] else ""
    request = f"SELECT count(*) FROM {table}{_where}"
    return CURSOR.execute(request).fetchall()[0][0]


def read(table: str = "lastrow", _where: dict = {}) -> list:
    """Reading records in a table"""
    column_list = "*"
    for fraction in _where.keys():
        column_list = ", ".join(_where[fraction].keys())
        _where = f" WHERE Fraction = '{fraction}'"
    request = f"SELECT {column_list} FROM {table}{_where if _where != {} else ''}"
    return CURSOR.execute(request).fetchall()


def write(rows: Union[tuple, list], table: str = "games") -> None:
    """Writing data to tables"""
    if type(rows) == tuple:
        request = f"INSERT INTO {table} {request_header(table)} VALUES {rows}"
        CURSOR.execute(request, rows)
    else:
        request = f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)"
        CURSOR.executemany(request, rows)
    CONN.commit()


def update(row: list) -> None:
    """Updates the entry in table 'lastrow'"""
    _set = settostr(zip(games_title, row))
    request = f"UPDATE lastrow SET {_set} WHERE rowid = 1"
    CURSOR.execute(request)
    CONN.commit()


def drop(table: str = "lastrow") -> None:
    """Drops the table"""
    CURSOR.execute(f"DROP TABLE {table}")
    CONN.commit()
