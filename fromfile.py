from bs4 import BeautifulSoup as soup
import table as tb
from support import modifyrows, log
import toml
import csv

# config
CFG = toml.load("config.toml")
HTML_DATA = dict(CFG["html_fraction"])
HTML_FILE = CFG["html_file"]
CSV_FILE = CFG["csv_file"]


def parsehtml(filename: str) -> list:
    """Parsed html file"""
    with open(filename, "r", encoding="utf-8") as f:
        contents = f.read()
        sp = soup(contents, "lxml")
        return [tuple(row) for row in sp.tbody.find_all("tr")]


def from_html(filename: str = HTML_FILE) -> list:
    """Import data from html file"""
    rows = list(modifyrows(HTML_DATA, parsehtml(filename)))
    if tb.count("lastrow") == 0:
        tb.write(rows[0], "lastrow")
        num_lastrow = len(rows)
    else:
        lastrow = tb.read()[0]
        num_lastrow = rows.index(lastrow)
    tb.update(rows[0])
    log(num_lastrow)
    return rows[:num_lastrow]


def from_csv(filename: str = CSV_FILE) -> list:
    """Import data from csv file"""
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        rows_from_csv = [tuple(row) for row in reader]
    log(len(rows_from_csv))
    return rows_from_csv


def import_file(import_from: int) -> list:
    """Choising import method"""
    if import_from == 1:
        return from_html()
    else:
        return from_csv() if import_from == 2 else None
