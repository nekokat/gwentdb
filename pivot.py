from support import wheretostr, settostr
import table as tb
from collections import defaultdict
from connection import CONN, CURSOR
import toml


# config
CFG = toml.load("config.toml")
FRACTIONS = dict(CFG["fraction"])
RESULT = dict(CFG["result"])


def read(table: str, _where: dict = {}) -> list:
    """Reading data from a pivot table"""
    if table in ["win_loss", "versus"]:
        return tb.read(table, _where)
    elif table in ["overall"]:
        fraction = ("Overall, " + FRACTIONS[_where]) if _where != {} else "*"
        request = f"SELECT {fraction} FROM overall"
    return CURSOR.execute(request).fetchall()


def update(rows: list, table: str) -> None:
    """Updating data in a pivot table"""
    _update = create_update(rows, table)
    for fraction in _update.keys():
        select_where = _update[fraction]
        if table in ["win_loss", "versus"]:
            set_where = set_where_winloss_versus(table, fraction, select_where)
        elif table == "overall":
            if select_where["Win"] == 0:
                continue
            set_where = set_where_overall(fraction, select_where)
        request = "UPDATE {} SET {} WHERE {}".format(table, *set_where)
        CURSOR.execute(request)
        CONN.commit()


def create_update(rows: list, table: str) -> dict:
    """Formation of a dictionary that contains data for updating in pivot tables"""
    table_header, position = (
        [RESULT, -2] if table in ["win_loss", "overall"] else [FRACTIONS, 3]
    )
    _update = defaultdict(lambda: defaultdict(int))
    for col in rows:
        _update[col[1]][table_header[col[position]]] += 1
    return _update


def set_where_winloss_versus(table: str, fraction: str, select_where) -> tuple:
    """Conditions for updating tables ('win_loss' or 'versus')"""
    select = read(table, {fraction: select_where})
    _select = map(sum, zip(*select, select_where.values()))
    _set = settostr(zip(select_where.keys(), _select))
    _where = wheretostr([("Fraction", fraction)])
    return (_set, _where)


def set_where_overall(fraction: str, select_where) -> tuple:
    """Conditions for updating table 'overall'"""
    select = read("overall", fraction)
    _select = map(sum, zip(*select, [select_where["Win"]] * 2))
    _set = settostr(zip(["Overall", FRACTIONS[fraction]], _select))
    _where = "rowid = 1"
    return (_set, _where)


def write(table: str) -> None:   
    """Writing data to pivot table"""
    if table in ("win_loss", "versus"):
        write_winloss_versus_table(table)
    elif table in ("overall"):
        write_overal_table(table)


def write_winloss_versus_table(table: str) -> None:
    """Writing data to 'win_loss' or 'versus' table"""
    header, column = (
        [RESULT, "result"] if table == "win_loss" else [FRACTIONS, "opponent_fraction"]
    )
    for fraction in FRACTIONS.keys():
        column_count = tuple(
            tb.count("games", [("fraction", fraction), (column, value)])
            for value in header.keys()
        )
        row = (fraction,) + column_count
        tb.write(row, table)


def write_overal_table(table: str) -> None:
    """Writing data to 'overall' table"""
    overall = tuple(
        tb.count("games", [("fraction", fraction), ("result", "Победа")])
        for fraction in FRACTIONS.keys()
    )
    row = (sum(overall),) + overall
    tb.write(row, table)


def update_all(rows: list, tables: list = ["win_loss", "versus", "overall"]) -> None:
    """ГUpdating all pivot tables"""
    [update(rows, table) for table in tables]


print("overall", sorted(read("overall")[0], reverse=True))

'''
request = "UPDATE overall SET Overall = '15763', Scoia’tael = '2830' WHERE rowid = 1"
CURSOR.execute(request)
CONN.commit()
'''

