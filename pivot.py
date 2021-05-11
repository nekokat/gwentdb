from support import wheretostr
from collections import defaultdict
from connection import CONN, CURSOR
import toml

#config
cfg = toml.load('config.toml')
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

def read(table, _where = {}, column_list = "*"):
  #solved
  if table in ['win_loss', 'versus']:
    for fraction in _where.keys():          
      column_list = ", ".join(_where[fraction].keys())
      _where = f" WHERE Fraction = '{fraction}'"
    request = f"SELECT {column_list} FROM {table}{_where if _where != {} else ''}"
  elif table in ['overall']:
    fraction = ('Overall, ' + fractions[_where]) if _where != {} else '*'
    request = f"SELECT {fraction} FROM overall"
  return CURSOR.execute(request).fetchall()

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
    CURSOR.execute(request)
    CONN.commit()

def updateall(rows, tables = ['win_loss', 'versus', 'overall']):
  #solved
  [update(rows, table) for table in tables]

