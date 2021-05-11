import toml

#config
cfg = toml.load('config.toml')
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

main_title = ('game_mode', 'fraction', 'opponent', 'opponent_fraction', 'result', 'score')

def request_header(table):
  table_header = result if table == 'win_loss' else fractions
  if table in ['win_loss', 'versus']:
    column_list = ('Fraction',) + tuple(table_header.values())
  elif table == 'overall':
    column_list = ('Overall',) + tuple(table_header.values())
  elif table in ['games', 'lastrow']:
    column_list = main_title
  return column_list

def modifyrows(html_data ,rows):
  #solved
  for row in rows:
    opp_fraction = html_data[row[3].i['class'][1]]
    result_score = row[4].text.split(" ")
    yield (row[0].text, row[2].text, row[3].text, opp_fraction, *result_score)

def wheretostr(_where, jumper= ", "):
  return jumper.join([f"{column} = '{value}'" for column, value in _where])

def log(countrows=0):
  #solved
  print(f'\nAdded: {countrows} rows.')
  print('Done')