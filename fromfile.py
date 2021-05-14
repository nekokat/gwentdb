from bs4 import BeautifulSoup as soup
import table as tb
from support import modifyrows, log
import toml
import csv

# config
cfg = toml.load("config.toml")
html_data = dict(cfg["html_fraction"])
html_file = cfg["html_file"]
csv_file = cfg["csv_file"]


def from_html():
    # solved
    # html parsing
    with open(html_file, "r", encoding="utf-8") as f:
        contents = f.read()
        sp = soup(contents, "lxml")
        rows = [tuple(row) for row in sp.tbody.find_all("tr")]
    # corrected row
    rows = list(modifyrows(html_data, rows))
    if tb.count("lastrow") == 0:
        tb.write(rows[0], "lastrow")
        num_lastrow = len(rows)
    else:
        lastrow = tb.read()[0]
        num_lastrow = rows.index(lastrow)
    tb.update(rows[0])
    log(num_lastrow)
    return rows[:num_lastrow]


def from_csv(filename=csv_file):
    # solved
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        rows_from_csv = [tuple(row) for row in reader]
    log(len(rows_from_csv))
    return rows_from_csv


def import_file(import_from):
    # solved
    if import_from == 1:
        return from_html()
    else:
        return from_csv() if import_from == 2 else None
