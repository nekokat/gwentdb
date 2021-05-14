import toml
import table as tb
from support import request_header
from connection import CONN, CURSOR

# config
cfg = toml.load("config.toml")
fractions = dict(cfg["fraction"])
result = dict(cfg["result"])
# tables
main_table = ("lastrow", "games")


def table_header(table):
    # solved
    header = request_header(table)
    if table in main_table:
        types = ("TEXT",) * len(header)
    elif table in ["win_loss", "versus"]:
        types = ("TEXT",) + ("INTEGER",) * (len(header) - 1)
    elif table in ["overall"]:
        types = ("INTEGER",) * len(header)
    title = [f'"{col}" {col_type}' for col, col_type in zip(header, types)]
    return "({})".format(", ".join(title))


def create(table):
    # solved
    request = f"CREATE TABLE {table} {table_header(table)}"
    CURSOR.execute(request)
    CONN.commit()


def create_pivot(table):
    # solved
    create(table)
    header, column = (
        [result, "result"] if table == "win_loss" else [fractions, "opponent_fraction"]
    )
    if table in ("win_loss", "versus"):
        for fraction in fractions.keys():
            column_count = tuple(
                tb.count("games", [("fraction", fraction), (column, value)])
                for value in header.keys()
            )
            row = (fraction,) + column_count
            tb.write(row, table)

    elif table in ("overall"):
        overall = tuple(
            tb.count("games", [("fraction", fraction), ("result", "Победа")])
            for fraction in fractions.keys()
        )
        row = (sum(overall),) + overall
        tb.write(row, table)


def createall():
    # solved
    for table in main_table:
        create(table)
    for table in ("win_loss", "versus", "overall"):
        create_pivot(table)
