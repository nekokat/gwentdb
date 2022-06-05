from sql import Sql as Query

r = Query()

CONN = r.connection
CURSOR = r.cursor

print(CONN, CURSOR)
