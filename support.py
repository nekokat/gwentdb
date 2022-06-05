import toml
from typing import Iterable, Any

# config
cfg = toml.load("config.toml")
FRACTIONS = dict(cfg["fraction"])
RESULT = dict(cfg["result"])

main_title = (
    "game_mode",
    "fraction",
    "opponent",
    "opponent_fraction",
    "result",
    "score",
)


def request_header(table: str) -> tuple:
    """Creating a tuple for a database query"""
    header = RESULT if table == "win_loss" else FRACTIONS
    columns = tuple(header.values())
    table_header = None
    if table in ["win_loss", "versus"]:
        table_header = ("Fraction",) + columns
    elif table == "overall":
        table_header = ("Overall",) + columns
    elif table in ["games", "lastrow"]:
        table_header = main_title
    return table_header


def modify_rows(html_data: dict, rows: list) -> Iterable[tuple]:
    """Preparing rows for writing to a table"""
    for row in rows:
        opp_fraction = html_data[row[3].i["class"][1]]
        result_score = row[4].text.split(" ")
        yield row[0].text, row[2].text, row[3].text, opp_fraction, *result_score


def to_str(_set_where: Any, delimiter: str = ", ") -> str:
    """Creates a 'set' and 'where' clause to query a database query"""
    set_where = [f"{column} = '{value}'" for column, value in _set_where]
    return delimiter.join(set_where)


def log(count_rows: int = 0) -> None:
    """Informs about the number of added records per session"""
    print(f"\nAdded: {count_rows} rows.")
    print("Done")
