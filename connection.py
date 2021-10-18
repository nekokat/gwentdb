"""Opening the database"""
import sqlite3
import toml

# config
CFG = toml.load("config.toml")
DATABASE_NAME = CFG["database"]

# database
CONN = sqlite3.connect(DATABASE_NAME)
CURSOR = CONN.cursor()
