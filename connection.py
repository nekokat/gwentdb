import sqlite3
import toml

CFG = toml.load("config.toml")
DATABASE_NAME = CFG["database"]

CONN = sqlite3.connect(DATABASE_NAME)
CURSOR = CONN.cursor()
