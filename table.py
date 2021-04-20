import sqlite3
import toml

#config
cfg = toml.load('config.toml')
name_data = cfg['database']

#database
conn = sqlite3.connect(name_data)
cursor = conn.cursor()

def create(table = 'lastrow'):
  cursor.execute(f'''CREATE TABLE {table} (game_mode text, fraction text,
  opponent text, opponent_fraction text, result text, score text)''')
  conn.commit()

def read(table = 'lastrow'):
  bol = cursor.execute(f"SELECT count(*) FROM {table}").fetchall()[0][0]
  if bol != 0:
    return cursor.execute(f'SELECT * FROM {table}').fetchall()[0]

def write(row, table = 'lastrow'):
  cursor.executemany(f"INSERT INTO {table} VALUES (?,?,?,?,?,?)", row)
  conn.commit()

def update(row, idx = 1, table = 'lastrow'):
  data = '''game_mode = "{}", fraction = "{}", opponent = "{}",
  opponent_fraction = "{}", result = "{}", score = "{}"'''.format(*row)
  
  cursor.execute(f"UPDATE {table} SET " + data + f" WHERE rowid = {idx}")
  conn.commit()

def drop(table = 'lastrow'):
  cursor.execute(f'DROP TABLE {table}')
  conn.commit()
