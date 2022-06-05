from sql import Sql as Query

r = Query()

rows = ('Обычный', 'Нильфгаард', 'jardelxl', 'Скоя’таэли', 'Поражение', '1:2')
header = ("game_mode", "fraction", "opponent", "opponent_fraction", "result", "score")
r.update("lastrow").set(score="1:2").where(rowid=1).execute()
r.commit()

