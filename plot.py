import pandas as pd
import table as tb
from support import request_header


def print_table(table):
    header = request_header(table)
    pd.set_option("display.max_columns", None)
    df = pd.DataFrame(tb.read(table), columns=header)
    print(df)
