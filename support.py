from lxml.html import parse, HTMLParser
import table as tb
import toml
import csv

partition = lambda l, n = 2: [l[i:i+n] for i in range(0, len(l), n)]
trans = lambda x: list(map(tuple, zip(*x)))

#config
cfg = toml.load('config.toml')
data = dict(cfg['fr_list'])
inp = cfg["input"]
csv_file = cfg['csv_file']

lastrow = tb.read()

#html parsing
page = parse(inp.encode("utf-8"), HTMLParser(encoding="utf-8"))
col = trans(partition(page.xpath('//tr//td/text()'), 5))

#fractions
fr, op_fr = trans(partition([data[i.attrib['class']] for i in page.xpath('//i')]))

#result & score
res_sc = trans(map(lambda x: x.split(" "), col[4]))

#fresh data
lines = trans([col[0], fr, col[3], op_fr] + res_sc)

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