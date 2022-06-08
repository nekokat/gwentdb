from draw_it import Printify
from sql import request_header
import table as tb

versus = Printify("versus")
versus.header = request_header(versus.table_name)
versus.add_rows(tb.read(versus.table_name))
print(versus)

win_loss = Printify("win_loss")
win_loss.header = request_header(win_loss.table_name)
win_loss.add_rows(tb.read(win_loss.table_name))
print(win_loss)

overall = Printify("overall")
overall.header = request_header(overall.table_name)
overall.add_rows(tb.read(overall.table_name))
print(overall)
