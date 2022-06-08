from typing import Tuple, Union, Any
from sql import Query, and_
import table as tb
from collections import defaultdict
import toml

CFG = toml.load("config.toml")
FRACTIONS = dict(CFG["fraction"])
RESULT = dict(CFG["result"])

q = Query()


def read(table: str, columns: Union[list, str], **kwargs) -> Union[list, Any]:
    """Reading data from a pivot table"""
    if table in ["win_loss", "versus"]:
        return tb.read(table, columns, **kwargs)
    elif table == "overall":
        fraction = ("Overall, " + FRACTIONS[columns]) if columns != "*" else "*"
        return q.select("overall", fraction).where(**kwargs).execute().fetchall()


def update(rows: list, table: str) -> None:
    """Updating data in a pivot table"""
    _update = create_update(rows, table)
    for fraction in _update.keys():
        set_where = setwhere(table, fraction, _update)
        if set_where == tuple():
            continue
        q.update(table).set(**set_where[0]).where(**set_where[1]).execute().commit()


def setwhere(table: str, fraction: str, _update: dict) -> tuple:
    select_where = _update[fraction]
    if table in ["win_loss", "versus"]:
        return set_where_winlossversus(table, fraction, select_where)
    elif table == "overall":
        if select_where["Win"] == 0:
            return tuple()
        return set_where_overall(fraction, select_where)


def create_update(rows: list, table: str) -> dict:
    """Formation of a dictionary that contains data
        for updating in pivot tables"""
    table_header, position = (
        [RESULT, -2] if table in ["win_loss", "overall"] else [FRACTIONS, 3]
    )
    _update = defaultdict(lambda: defaultdict(int))
    for col in rows:
        _update[col[1]][table_header[col[position]]] += 1
    return _update


def set_where_winlossversus(table: str, fraction: str, select_where: dict) -> tuple:
    """Conditions for updating tables ('win_loss' or 'versus')"""
    select = read(table, list(select_where.keys()), Fraction=fraction)
    _select = list(map(sum, zip(*select, select_where.values())))
    _set = dict(zip(select_where.keys(), _select))
    _where = {"Fraction": fraction}
    return _set, _where


def set_where_overall(fraction: str, select_where: dict) -> tuple:
    """Conditions for updating table 'overall'"""
    select = read("overall", columns=fraction)
    _select = map(sum, zip(*select, [select_where["Win"]] * 2))
    _set = dict(zip(["Overall", FRACTIONS[fraction]], _select))
    _where = {"rowid": 1}
    return _set, _where


def write(table: str) -> None:
    """Writing data to pivot table"""
    if table in ("win_loss", "versus"):
        write_winlossversus_table(table)
    elif table in "overall":
        write_overal_table(table)


def write_winlossversus_table(table: str) -> None:
    """Writing data to 'win_loss' or 'versus' table"""
    header, column = (
        [RESULT, "result"] if table == "win_loss" else [
            FRACTIONS, "opponent_fraction"]
    )
    for fraction in FRACTIONS.keys():
        column_count: Tuple[int] = tuple(
            tb.count("games", **dict([("fraction", fraction), (column, value)]))
            for value in header.keys()
        )
        row = (fraction,) + column_count
        q.insert(table).execute(row).commit()


def write_overal_table(table: str) -> None:
    """Writing data to 'overall' table"""
    overall = tuple(
        q.select("games", 'count(*)').where(and_(fraction=fraction, result="Победа")).execute().fetchall()[0][0]
        for fraction in FRACTIONS.keys()
    )
    row = (sum(overall),) + overall
    q.insert(table).execute(row).commit()


def update_all(rows: list, tables=None) -> None:
    """Updating all pivot tables"""
    if tables is None:
        tables = ["win_loss", "versus", "overall"]
    [update(rows, table) for table in tables]


print("overall", sorted(read("overall", "*")[0], reverse=True))
