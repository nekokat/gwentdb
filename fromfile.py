from typing import Iterable
from bs4 import BeautifulSoup as Soup
import table as tb
import toml
import csv

# config
CFG = toml.load("config.toml")
HTML_DATA = dict(CFG["html_fraction"])
HTML_FILE = CFG["html_file"]
CSV_FILE = CFG["csv_file"]


def _log(count_rows: int = 0) -> None:
    """Informs about the number of added records per session"""
    print(f"\nAdded: {count_rows} rows.")
    print("Done")


def _modify_rows(html_data: dict, rows: list) -> Iterable[tuple]:
    """Preparing rows for writing to a table"""
    for row in rows:
        opp_fraction = html_data[row[3].i["class"][1]]
        result_score = row[4].text.split(" ")
        yield row[0].text, row[2].text, row[3].text, opp_fraction, *result_score


def parsehtml(filename: str) -> list:
    """Parsed html file"""
    with open(filename, "r", encoding="utf-8") as f:
        contents = f.read()
        sp = Soup(contents, "lxml")
        return [tuple(row) for row in sp.tbody.find_all("tr")]


def from_html(filename: str = HTML_FILE) -> list:
    """Import data from html file"""
    rows = list(_modify_rows(HTML_DATA, parsehtml(filename)))
    if tb.count("lastrow") == 0:
        tb.write(rows[0], "lastrow")
        num_lastrow = len(rows)
    else:
        lastrow = tb.read("lastrow", rowid=1)[0]
        num_lastrow = rows.index(lastrow)
    tb.update(rows[0])
    _log(num_lastrow)
    return rows[:num_lastrow]


def from_csv(filename: str = CSV_FILE) -> list:
    """Import data from csv file"""
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        rows_from_csv = [tuple(row) for row in reader]
    _log(len(rows_from_csv))
    return rows_from_csv


def import_file(import_from: int) -> list:
    """Choice import method"""
    if import_from == 1:
        return from_html()
    else:
        return from_csv() if import_from == 2 else None
