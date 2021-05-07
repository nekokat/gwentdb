import sqlite3
import toml
import table as tb
from support import сondition

#config
cfg = toml.load('config.toml')
name_database = cfg['database']
fraction = dict(cfg['fraction'])
result = dict(cfg['result'])

#database
conn = sqlite3.connect(name_database)
cursor = conn.cursor()

def header(table):
  res = result if table == 'win_loss' else fraction
  return ", ".join(res.values())

def create(table):
  tb.create(table)
  if table in ['win_loss', 'versus']:
    table_header, column = [result, 'result'] if table == 'win_loss' else [fraction, 'opponent_fraction']
    for frkey in fraction.keys():
      column_count = tuple(tb.count([('fraction', frkey),(column, colkey)]) for colkey in table_header.keys())
      row = (frkey,) + column_count
      request = f"INSERT INTO {table} ({header(table)}) VALUES {row}"
      cursor.execute(request)
  conn.commit()

def update(row, table):
  from collections import defaultdict
  table_header, position = [result, -2] if table == 'win_loss' else [fraction, 3]
  new_data = defaultdict(lambda: defaultdict(int))
  for item in row:
    new_data[item[1]][item[position]] += 1
  for col in new_data.keys():
    column = new_data[col]
    _set = сondition([(table_header[key], column[key]) for key in column.keys()])
    _where = сondition([('Fraction', col)])
    request = f"UPDATE {table} SET {_set} WHERE {_where}"
    print(request)
    #cursor.execute(request)
    #conn.commit()

    
'''
drop('versus')
drop('win_loss')
create_pivot('versus')
create_pivot('win_loss')
'''
row = [('Обычный', 'Чудовища', 'leniolek13', 'Скоя’таэли', 'Победа', '2:0'), ('Обычный', 'Чудовища', 'SeaJackal', 'Чудовища', 'Поражение', '1:2'), ('Обычный', 'Чудовища', 'Sean_Lai97', 'Королевства Севера', 'Поражение', '0:2'), ('Обычный', 'Чудовища', '大碗凉粉', 'Нильфгаард', 'Поражение', '1:2'), ('Обычный', 'Чудовища', 'Empty_key', 'Скоя’таэли', 'Победа', '2:0'), ('Обычный', 'Чудовища', 'de60ne', 'Скоя’таэли', 'Поражение', '1:2'), ('Обычный', 'Чудовища', 'JakakArtem', 'Нильфгаард', 'Поражение', '1:2'), ('Обычный', 'Нильфгаард', 'dairokutenmaho', 'Скоя’таэли', 'Поражение', '1:2'), ('Обычный', 'Нильфгаард', 'Malerganon', 'Чудовища', 'Ничья', '2:2'), ('Обычный', 'Нильфгаард', 'cclingg', 'Скоя’таэли', 'Поражение', '1:2'), ('Обычный', 'Нильфгаард', 'leshkadoc', 'Нильфгаард', 'Победа', '2:0'), ('Обычный', 'Нильфгаард', 'Ruthlessmurder', 'Чудовища', 'Поражение', '0:2'), ('Обычный', 'Чудовища', 'TrinalAlloy471', 'Нильфгаард', 'Победа', '2:1')]