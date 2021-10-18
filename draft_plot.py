from support import request_header
from typing import Iterable, Union
import table as tb
import toml

CFG = toml.load("border_config.toml")
TOP_LINE = dict(CFG["top_line"])
MIDDLE_LINE = dict(CFG["middle_line"])
ROW_SEPARATOR = CFG["row_separator"]
BOTTOM_LINE = dict(CFG["bottom_line"])


class Border:
    """Table border symbols"""

    def __init__(self):
        self.top_line = TOP_LINE
        self.middle_line = MIDDLE_LINE
        self.bottom_line = BOTTOM_LINE
        self._row_separator = ROW_SEPARATOR
        self.row = self.row_style(self._row_separator)
        self._column_size = list()

    def row_style(self, sep: str) -> dict:
        return {
            "left": sep.ljust(2),
            "right": sep.rjust(2),
            "sep": sep.center(3),
        }

    def draw_line(self, line_style: dict) -> str:

        draw = line_style["left"]
        draw += line_style["sep"].join(
            line_style["line"] * (column + 2) for column in self._column_size
        )
        draw += line_style["right"]
        return draw

    def draw_top(self) -> str:
        return self.draw_line(self.top_line)

    def draw_middle(self) -> str:
        return self.draw_line(self.middle_line)

    def draw_bottom(self) -> str:
        return self.draw_line(self.bottom_line)

    def draw_row(self, row: tuple) -> str:
        line = self.row["left"]
        line += self.row["sep"].join(self.align(row))
        line += self.row["right"]
        return line

    def align(self, row: tuple) -> Iterable[str]:
        for col, just in zip(row, self._column_size):
            yield str(col).center(just)

    @property
    def row_separator(self) -> str:
        return self._row_separator

    @row_separator.setter
    def row_separator(self, sep: str) -> None:
        self._row_separator = sep
        self.row = self.row_style(sep)


class Printify:
    def __init__(self, table="New_Table"):
        self._table_name = table
        self._header = tuple()
        self._column_size = list()
        self._rows = list()
        self._border = Border()

    def column_width(self, row: tuple) -> list:
        return list(map(len, map(str, row)))

    def columns_width(self, rows: list) -> list:
        return list(self.column_width(row) for row in rows)

    def max_columns_width(self, row: Union[list, tuple]) -> int:
        if type(row) == tuple:
            width = [self.column_width(row)]
        elif type(row) == list:
            width = self.columns_width(row)
        column_size = list(map(max, zip(*width, self._column_size)))
        self._border._column_size = column_size
        return column_size

    def column_size(self, row: Union[list, tuple]) -> None:
        if self._column_size == list():
            self._column_size = [0] * len(self._header)
        self._column_size = self.max_columns_width(row)

    def add_row(self, row) -> None:
        self._rows.append(row)
        self.column_size(row)

    def add_rows(self, rows: list) -> None:
        self._rows.extend(rows)
        self.column_size(rows)

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, table: str) -> None:
        self._table_name = table

    @property
    def header(self) -> str:
        return self._header

    @header.setter
    def header(self, header: str) -> None:
        self._header = header
        self.column_size(header)

    def print_middle(self) -> str:
        sep = f"\n{self._border.draw_middle()}\n"
        data = [self._header, *self._rows]
        return f"\n{sep.join(self._border.draw_row(row) for row in data)}\n"

    def __str__(self) -> str:
        line = self._border.draw_top()
        line += self.print_middle()
        line += self._border.draw_bottom()
        line += f"\ntable '{self._table_name}'\n"
        return line


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
