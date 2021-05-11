import toml
from support import wheretostr
from connection import CONN, CURSOR

#config
cfg = toml.load('config.toml')
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

#table title
games_title = ['game_mode', 'fraction', 'opponent', 'opponent_fraction', 'result', 'score']

def count(table, _where = []):
  #solved 50/50
  request_where = f" WHERE {wheretostr(_where, ' AND ')}" if _where != [] else ''
  request = f"SELECT count(*) FROM {table}{request_where}"
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
  CURSOR.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", rows)
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
  
print('Programm is working, but...')
print('!!!!WARNING!!!! need to rewrite "read" (complite 30%) in pivot module')