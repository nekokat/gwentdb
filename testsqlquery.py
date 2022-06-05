from sql import Sql as Query

r = Query()

rows = ('Обычный', 'Нильфгаард', 'jardelxl', 'Скоя’таэли', 'Поражение', '2:2')
header = ("game_mode", "fraction", "opponent", "opponent_fraction", "result", "score")
r.update("lastrow").set(header, rows).where(rowid=1).execute().commit()
