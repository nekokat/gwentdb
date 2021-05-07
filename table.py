import sqlite3
import toml
import pivot as pv
from support import сondition

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
  def header():
    column_list = pv.header(table)
    if table in ['lastrow', 'games']:
      return "'{}'".format("','".join(games_title))
    elif table in ['win_loss', 'versus']:
      return "'Fraction', {}".format(column_list)
    elif table == 'overall':
      return "'Overall', {}".format(column_list)
  
  request = f"CREATE TABLE {table} ({header()})"
  cursor.execute(request)
  conn.commit()

def read(_where = {}, table = 'lastrow'):
  if table == 'lastrow' and count() != 0 and _where == {}:
    return cursor.execute(f'SELECT * FROM {table}').fetchall()[0]
  elif table in ['win_loss', 'versus']:
    column_list = pv.header(table)
    for fr in _where.keys():
      request = f"SELECT {column_list} FROM {table} WHERE Fraction = '{fr}'"
      print(cursor.execute(request).fetchall()[0])

def write(row, table = 'games'):
  if table in ['lastrow', 'games']:
    cursor.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", row)
  #print(pv.update(row, 'versus'))
  print(pv.update(row, 'win_loss'))
  conn.commit()

def update(row, table = 'lastrow'):
  if table in ['games', 'lastrow']:
    _set = сondition(list(zip(games_title, row)))
    _where = сondition([('rowid',1)])
    request = f"UPDATE {table} SET {_set} WHERE {_where}"
    cursor.execute(request)
  conn.commit()

def drop(table = 'lastrow'):
  cursor.execute(f'DROP TABLE {table}')
  conn.commit()