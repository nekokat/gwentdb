import sqlite3
import toml
from support import сondition, header

#config
cfg = toml.load('config.toml')
name_database = cfg['database']
fraction = dict(cfg['fraction'])
result = dict(cfg['result'])

#database
conn = sqlite3.connect(name_database)
cursor = conn.cursor()

#table title
games_title = ['game_mode', 'fraction', 'opponent', 'opponent_fraction', 'result', 'score']

def count(_where = [], table = 'games'):
  _where = " WHERE " + сondition(_where, " AND ") if _where != [] else ""
  request = f"SELECT count(*) FROM {table}{_where}"
  return cursor.execute(request).fetchall()[0][0]

def create(table = 'lastrow'):
  pivot_table = ['win_loss', 'versus', 'overall']
  def table_header():
    if table in ['lastrow', 'games']:
      return "'{}'".format("','".join(games_title))
    elif table in pivot_table:
      return header(table)
  request = f"CREATE TABLE {table} ({table_header()})"
  cursor.execute(request)
  conn.commit()

def read(_where = {}, table = 'lastrow'):
  if table == 'lastrow' and count() != 0 and _where == {}:
    return cursor.execute(f'SELECT * FROM {table}').fetchall()[0]
  elif table in ['win_loss', 'versus']:
    column_list = header(table)
    for fr in _where.keys():
      request = f"SELECT {column_list} FROM {table} WHERE Fraction = '{fr}'"
      print(cursor.execute(request).fetchall()[0])

def write(row, table = 'games'):
  if table in ['lastrow', 'games']:
    cursor.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", row)
  conn.commit()

def update(row, table = 'lastrow'):
  if table in ['games', 'lastrow']:
    _set = сondition(list(zip(games_title, row)))
    _where = "rowid = 1"
    request = f"UPDATE {table} SET {_set} WHERE {_where}"
    cursor.execute(request)
  conn.commit()

def drop(table = 'lastrow'):
  cursor.execute(f'DROP TABLE {table}')
  conn.commit()