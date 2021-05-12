import toml
from support import wheretostr, request_header
from connection import CONN, CURSOR

#config
cfg = toml.load('config.toml')
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

#table title
games_title = ['game_mode', 'fraction', 'opponent', 'opponent_fraction', 'result', 'score']

def count(table, _where = []):
  #solved 50/50
  _where = f" WHERE {wheretostr(_where, ' AND ')}" if _where != [] else ''
  request = f"SELECT count(*) FROM {table}{_where}"
  return CURSOR.execute(request).fetchall()[0][0]

def read(table = 'lastrow', _where = {}):
  #solved
  column_list = "*"
  for fraction in _where.keys():          
    column_list = ", ".join(_where[fraction].keys())
    _where = f" WHERE Fraction = '{fraction}'"
  request = f"SELECT {column_list} FROM {table}{_where if _where != {} else ''}"
  return CURSOR.execute(request).fetchall()

def write(rows, table = 'games'):
  #solved
  if type(rows) == tuple:
    request = f"INSERT INTO {table} {request_header(table)} VALUES {rows}"    
    print(request)
    CURSOR.execute(request, rows)
  else:
    request = f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)"
    print(request)
    CURSOR.executemany(request, rows)
  CONN.commit()

def update(row):
  #solved
  _set = wheretostr(zip(games_title, row))
  request = f"UPDATE lastrow SET {_set} WHERE rowid = 1"
  CURSOR.execute(request)
  CONN.commit()

def drop(table = 'lastrow'):
  #solved
  CURSOR.execute(f'DROP TABLE {table}')
  CONN.commit()