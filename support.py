import bs4
from bs4 import BeautifulSoup as soup
import table as tb
import toml
import csv

#config
cfg = toml.load('config.toml')
data = dict(cfg['fr_list'])
inp = cfg["input"]
csv_file = cfg['csv_file']

lastrow = tb.read()

#html parsing
with open(inp, "r") as f:
  contents = f.read() 
  sp = soup(contents, 'lxml') 
  lines = [tuple(j) for j in sp.tbody.find_all("tr")]

def modify(lines = lines):
  res = []
  for i in lines:
    opp_fr = data[i[3].i['class'][1]]
    result_score = i[4].text.split(" ")
    tpl = (i[0].text, i[2].text, i[3].text, opp_fr, *result_score)
    res.append(tpl)
  return res

lines = modify()

#lastrow id in fresh inputs data
num_line = lines.index(lastrow)

#corrected input_data
def from_html():
  return lines[:num_line] if lastrow in lines else lines

def from_csv(filename = csv_file):
  with open(filename, newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    return [tuple(row) for row in reader]

def from_file(import_from):
  if import_from == 1:
    return from_html()
  else:
    return from_csv() if import_from == 2 else []

def log(new_lines = num_line):
  print(f'\nAdded: {new_lines} lines.')
  print('Done')