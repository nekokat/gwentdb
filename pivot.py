from support import wheretostr
from collections import defaultdict
import sqlite3
import toml
import table as tb

#config
cfg = toml.load('config.toml')
name_database = cfg['database']
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

#database
conn = sqlite3.connect(name_database)
cursor = conn.cursor()

def request_header(table):
  #solved 50/50
  table_header = result if table == 'win_loss' else fractions
  column_list = "', '".join(table_header.values())
  if table in ['win_loss', 'versus']:
    column_list = "'Fraction', '{}'".format(column_list)
  elif table == 'overall':
    column_list = "'Overall', '{}'".format(column_list)
  return column_list

def create(table):
  #solved 50/50
  tb.create(table)
  table_header, column = [result,'result'] if table == 'win_loss' else [fractions,'opponent_fraction']
  if table in ['win_loss', 'versus']:
    for fraction in fractions.keys():
      column_count = tuple(tb.count('games', [('fraction', fraction),(column, value)]) for value in table_header.keys())
      row = (fraction,) + column_count
      request = f"INSERT INTO {table} ({request_header(table)}) VALUES {row}"
      cursor.execute(request)
      conn.commit()
  elif table in ['overall']:
    overall = tuple(tb.count('games', [('fraction', fraction),('result', 'Победа')]) for fraction in fractions.keys())
    row = (sum(overall),) + overall
    request = f"INSERT INTO {table} ({request_header(table)}) VALUES {row}"
    cursor.execute(request)
    conn.commit()

def read(table, _where = {}, column_list = "*"):
  #solved 75/25
  if table in ['win_loss', 'versus']:
    for fraction in _where.keys():          
      column_list = ", ".join(_where[fraction].keys())
      _where = f" WHERE Fraction = '{fraction}'"
    request = f"SELECT {column_list} FROM {table}{_where if _where != {} else ''}"
  elif table in ['overall']:
    fraction = fractions[_where] if _where != {} else '*'
    request = f"SELECT Overall, {fraction} FROM overall"
  return cursor.execute(request).fetchall()

def update(rows, table):
  #solved
  def settostr(_where):
    return ", ".join([f"{column} = {value}" for column, value in _where])
  table_header, position = [result, -2] if table in ['win_loss', 'overall'] else [fractions, 3]
  _update = defaultdict(lambda: defaultdict(int))
  for col in rows:
    _update[col[1]][table_header[col[position]]] += 1
  for fraction in _update.keys():
    select_where = _update[fraction]
    if table in ['win_loss', 'versus']:
      select = read(table, {fraction: select_where})
      _select = map(sum, zip(*select, select_where.values()))
      _set = settostr(zip(select_where.keys(), _select))
      _where = wheretostr([('Fraction', fraction)])
    elif table == 'overall':
      if select_where['Win'] == 0:
        continue
      select = read('overall', fraction)
      _select = map(sum, zip(*select, [select_where['Win']]*2))
      _set = settostr(zip(['Overall', fractions[fraction]], _select))
      _where = 'rowid = 1'
    request = f"UPDATE {table} SET {_set} WHERE {_where}"
    cursor.execute(request)
    conn.commit()

def updateall(rows, tables = ['win_loss', 'versus', 'overall']):
  #solved
  [update(rows, table) for table in tables]

rows = [('Обычный','Нильфгаард','Fire_Player','Чудовища','Поражение','1:2'),
('Обычный','Синдикат','_Yoozek_','Синдикат','Победа','2:0'),
('Обычный','Королевства Севера','Nagaika','Нильфгаард','Ничья','2:2')]
