import toml

#config
cfg = toml.load('config.toml')
fractions = dict(cfg['fraction'])
result = dict(cfg['result'])

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