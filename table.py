from sql import Query
from typing import Union, Iterable


q = Query()


def count(table: str, **kwargs) -> int:
    """Counts the number of rows for a given condition"""
    request = q.select(table, "count(*)").where(**kwargs).execute().fetchall()
    return request[0][0]


def read(table: str, columns: Union[str, list] = "*", **kwargs) -> list:
    """Reading records in a table"""
    return q.select(table, ",".join(columns)).where(**kwargs).execute().fetchall()


def write(rows: Union[tuple, list], table: str = "games") -> None:
    """Writing data to tables"""
    if type(rows) is tuple:
        q.insert(table).execute(rows).commit()
    elif type(rows) is list:
        q.insert(table).executemany(rows).commit()


def update(row: list) -> None:
    """Updates the entry in table 'lastrow'"""
    games_title = ("game_mode", "fraction", "opponent", "opponent_fraction", "result", "score",)
    q.update("lastrow").set(games_title, row).where(rowid=1).execute().commit()


def drop(table: str = "lastrow") -> None:
    """Drops the table"""
    q.drop(table).execute().commit()
