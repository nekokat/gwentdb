import sqlite3
import toml
from support import wheretostr

#config
cfg = toml.load('config.toml')
name_database = cfg['database']
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

#database
conn = sqlite3.connect(name_database)
cursor = conn.cursor()

#table title
games_title = ['game_mode', 'fraction', 'opponent', 'opponent_fraction', 'result', 'score']

def column_header(table):
  #solved 50/50
  table_header = result if table == 'win_loss' else fractions
  column_list = "', '".join([f"{col} INTEGER"for col in table_header.values()])
  if table in ['win_loss', 'versus']:
    column_list = "'Fraction TEXT', '{}'".format(column_list)
  elif table == 'overall':
    column_list = "'Overall INTEGER', '{}'".format(column_list)
  return column_list

def count(table = 'games', _where = []):
  #solved
  request = f"SELECT count(*) FROM {table}{_where if _where != [] else ''}"
  return cursor.execute(request).fetchall()[0][0]

def create(table = 'lastrow'):
  pivot_table = ['win_loss', 'versus', 'overall']
  def table_header():
    if table in ['lastrow', 'games']:
      return "'{}'".format("','".join([f'{col} TEXT' for col in games_title]))
    elif table in pivot_table:
      return column_header(table)
  request = f"CREATE TABLE {table} ({table_header()})"
  cursor.execute(request)
  conn.commit()

def read(table = 'lastrow', _where = {}, column_list = "*"):
  #solved 50/50
  for fraction in _where.keys():          
    column_list = ", ".join(_where[fraction].keys())
    _where = f" WHERE Fraction = '{fraction}'"
  request = f"SELECT {column_list} FROM {table}{_where if _where != {} else ''}"
  return cursor.execute(request).fetchall()

def write(rows, table = 'games'):
  #solved
  cursor.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", rows)
  conn.commit()

def update(row):
  #solved
  _set = wheretostr(zip(games_title, row))
  request = f"UPDATE lastrow SET {_set} WHERE rowid = 1"
  cursor.execute(request)
  conn.commit()

def drop(table = 'lastrow'):
  #solved
  cursor.execute(f'DROP TABLE {table}')
  conn.commit()

print('Programm is working, but...')
print('!!!!WARNING!!!! need to rewrite "read" complite for 50% in table module')
print('!!!!WARNING!!!! need to rewrite "create" complite for 50% in pivot module')