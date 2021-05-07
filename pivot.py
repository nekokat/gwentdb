from support import сondition, header
import sqlite3
import toml
import table as tb

#config
cfg = toml.load('config.toml')
name_database = cfg['database']
fraction = dict(cfg['fraction'])
result = dict(cfg['result'])

#database
conn = sqlite3.connect(name_database)
cursor = conn.cursor()

def create(table):
  tb.create(table)
  table_header = result if table == 'win_loss' else fraction
  if table in ['win_loss', 'versus']:
    column = ['opponent_fraction', 'result',][table == 'win_loss']
    for frkey in fraction.keys():
      column_count = tuple(tb.count([('fraction', frkey),(column, value)]) for value in table_header.keys())
      row = (frkey,) + column_count
      request = f"INSERT INTO {table} ({header(table)}) VALUES {row}"
      print(request)
      #cursor.execute(request)
  conn.commit()

def update(rows, table):
  from collections import defaultdict
  table_header, position = [result,-2] if table == 'win_loss' else [fraction, 3]
  new_data = defaultdict(lambda: defaultdict(int))
  for row in rows:
    new_data[row[1]][row[position]] += 1
  for col in new_data.keys():
    column = new_data[col]
    _set = сondition([(table_header[key], column[key]) for key in column.keys()])
    _where = сondition([('Fraction', col)])
    request = f"UPDATE {table} SET {_set} WHERE {_where}"
    #cursor.execute(request)
    #conn.commit()

def updateall(row, tables = ['win_loss', 'versus', 'overall']):
  for table in tables:
    update(row, table)