import sqlite3
import toml

#config
cfg = toml.load('config.toml')
name_data = cfg['database']
fr = cfg['fraction']
result = cfg['result']

#database
conn = sqlite3.connect(name_data)
cursor = conn.cursor()

#support
dt = lambda x, y= ", ": y.join([f"{i} = '{j}'" for i,j in x])

def create(table = 'lastrow'):
  header = f"({ciu('c', table)})"
  cursor.execute(f'CREATE TABLE {table} {header}')
  conn.commit()

def read(table = 'lastrow'):
  if count() != 0:
    return cursor.execute(f'SELECT * FROM {table}').fetchall()[0]

def write(row, table = 'games'):
  if table in ['lastrow', 'games']:
    cursor.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", row)
  conn.commit()

def pivot(table):
  tr, dt = [result, 'result'] if table == 'win_loss' else [fr, 'opponent_fraction']
  for i in fr:
    x = tuple(count(condition = [('fraction', i),(dt ,j)]) for j in tr)
    col = (i,) + x + (sum(x),)
    cursor.execute("INSERT INTO {} ('Fraction', '{}', 'Total') VALUES {}".format(table,"', '".join(tr), col))
  conn.commit()

def update(row, table = 'lastrow'):
  data = ciu('c', table).split(", ")
  if table in ['games', 'lastrow']:
    name = dt([('rowid',1)])
    text = f"UPDATE {table} SET " + dt(list(zip(data, row))) + f" WHERE {name}"
    print(text)
  elif table in ['win_loss', 'versus']:
    name = 'Fraction'

  cursor.execute(text)
  conn.commit()

def drop(table = 'lastrow'):
  cursor.execute(f'DROP TABLE {table}')
  conn.commit()

def ciu(execute_type, table):
  rs = result if table == 'win_loss' else fr
  if execute_type == 'c':
    if table in ['lastrow', 'games']:
      return "'game_mode', 'fraction', 'opponent', 'opponent_fraction', 'result', 'score'"
    elif table in ['win_loss', 'versus']:
      return "'Fraction', '{}', 'Total'".format("', '".join(rs))
  elif execute_type == 'i':
    None
  elif execute_type == 'u':
    None

def count(table = 'games', condition = []):
  cond = " WHERE " + dt(condition, " AND ") if condition != [] else ""
  return cursor.execute(f"SELECT count(*) FROM {table}{cond}").fetchall()[0][0]

def injection ():
  None

'''
drop('versus')
drop('win_loss')
create('win_loss')
create('versus')
pivot('versus')
pivot('win_loss')
'''
print(dt([('rowid',1)]))