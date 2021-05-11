import sqlite3
import toml

#config
cfg = toml.load('config.toml')
name_database = cfg['database']

#database
CONN = sqlite3.connect(name_database)
CURSOR = CONN.cursor()