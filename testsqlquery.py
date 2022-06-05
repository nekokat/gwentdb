from sql import Sql as Query

r = Query()

print(r.select("lastrow").execute().fetchall())
r.commit()
