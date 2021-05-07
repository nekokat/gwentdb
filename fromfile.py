from bs4 import BeautifulSoup as soup
import table as tb
from support import modifyrows, log
import toml
import csv

#config
cfg = toml.load('config.toml')
html_data = dict(cfg['html_fraction'])
inp = cfg["input"]
csv_file = cfg['csv_file']

#corrected input_data
def from_html():
  #html parsing
  with open(inp, "r") as f:
    contents = f.read() 
    sp = soup(contents, 'lxml') 
    rows = [tuple(j) for j in sp.tbody.find_all("tr")]
  lastrow = tb.read()
  rows = modifyrows(html_data, rows)
  #lastrow id in fresh inputs data
  num_lastrow = rows.index(lastrow)
  log(num_lastrow)
  return rows[:num_lastrow] if lastrow in rows else rows

def from_csv(filename = csv_file):
  with open(filename, newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    rows_from_csv = [tuple(row) for row in reader]
  log(len(rows_from_csv))
  return rows_from_csv

def import_file(import_from):
  if import_from == 1:
    return from_html()
  else:
    return from_csv() if import_from == 2 else None