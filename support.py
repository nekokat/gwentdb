import bs4
from bs4 import BeautifulSoup as soup
import table as tb
import toml
import csv

#config
cfg = toml.load('config.toml')
html_data = dict(cfg['html_fraction'])
inp = cfg["input"]
csv_file = cfg['csv_file']

lastrow = tb.read()

#html parsing
with open(inp, "r") as f:
  contents = f.read() 
  sp = soup(contents, 'lxml') 
  rows = [tuple(j) for j in sp.tbody.find_all("tr")]

def modifyrows(rows = rows):
  modrows = []
  for i in rows:
    opp_fraction = html_data[i[3].i['class'][1]]
    result_score = i[4].text.split(" ")
    row = (i[0].text, i[2].text, i[3].text, opp_fraction, *result_score)
    modrows.append(row)
  return modrows

rows = modifyrows()

#lastrow id in fresh inputs data
num_lastrow = rows.index(lastrow)

#corrected input_data
def from_html():
  return rows[:num_lastrow] if lastrow in rows else rows

def from_csv(filename = csv_file):
  with open(filename, newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    return [tuple(row) for row in reader]

def import_file(import_from):
  if import_from == 1:
    return from_html()
  else:
    return from_csv() if import_from == 2 else []

def сondition(cond, jumper= ", ")
  return jumper.join([f"{column} = '{value}'" for column, value in cond])

def log(countrows = num_lastrow):
  print(f'\nAdded: {countrows} rows.')
  print('Done')