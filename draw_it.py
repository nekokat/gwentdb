import toml
from support import request_header
from typing import Iterable, Union
import table as tb


CFG = toml.load("border_config.toml")
TOP_LINE = dict(CFG["top_line"])
MIDDLE_LINE = dict(CFG["middle_line"])
BOTTOM_LINE = dict(CFG["bottom_line"])
ROW_SEPARATOR = CFG["row_separator"]


class Border:
    """Table border symbols"""

    def __init__(self) -> None:
        self.top_line = TOP_LINE
        self.middle_line = MIDDLE_LINE
        self.bottom_line = BOTTOM_LINE
        self._row_separator = ROW_SEPARATOR
        self.row = self.row_style(self._row_separator)
        self._column_size = list()

    def row_style(self, sep: str) -> dict:
        """Generates formatted cell border elements (relative to text)
            based on self._row_separator"""
        return {
            "left": sep.ljust(2),
            "right": sep.rjust(2),
            "sep": sep.center(3),
        }

    def draw_line(self, line_style: dict) -> str:
        """Responsible for the formation of borders (does not contain data)"""
        draw = line_style["left"]
        draw += line_style["sep"].join(
            line_style["line"] * (column + 2) for column in self._column_size
        )
        draw += line_style["right"]
        return draw

    def draw_top(self) -> str:
        """Drawing the top border"""
        return self.draw_line(self.top_line)

    def draw_middle(self) -> str:
        """Drawing the middle border"""
        return self.draw_line(self.middle_line)

    def draw_bottom(self) -> str:
        """Drawing the bottom border"""
        return self.draw_line(self.bottom_line)

    def draw_row(self, row: tuple) -> str:
        """Drawing the row with data"""
        line = self.row["left"]
        line += self.row["sep"].join(self.align(row))
        line += self.row["right"]
        return line

    def align(self, row: tuple) -> Iterable[str]:
        """Content alignment"""
        for col, just in zip(row, self._column_size):
            yield str(col).center(just)

    @property
    def row_separator(self) -> str:
        """Returns the separator"""
        return self._row_separator

    @row_separator.setter
    def row_separator(self, sep: str) -> None:
        """Separator assignment"""
        self._row_separator = sep
        self.row = self.row_style(sep)


class Printify:
    """Print table data"""

    def __init__(self, table: str = "New_Table") -> None:
        self._table_name = table
        self._header = tuple()
        self._column_size = list()
        self._rows = list()
        self._border = Border()

    def column_width(self, row: tuple) -> list:
        """Helper for function 'max_columns_width' if 'row' is 'tuple'."""
        return list(map(len, map(str, row)))

    def columns_width(self, rows: list) -> list:
        """Helper for function 'max_columns_width' if 'row' is 'list'."""
        return list(self.column_width(row) for row in rows)

    def max_columns_width(self, row: Union[list, tuple]) -> int:
        """Specifies the maximum possible field size"""
        if type(row) == tuple:
            width = [self.column_width(row)]
        elif type(row) == list:
            width = self.columns_width(row)
        column_size = list(map(max, zip(*width, self._column_size)))
        self._border._column_size = column_size
        return column_size

    def column_size(self, row: Union[list, tuple]) -> None:
        """Column size"""
        if self._column_size == list():
            self._column_size = [0] * len(self._header)
        self._column_size = self.max_columns_width(row)

    def add_row(self, row: list) -> None:
        """Adds one line with data in table for printing"""
        self._rows.append(row)
        self.column_size(row)

    def add_rows(self, rows: list) -> None:
        """Adds several lines with data in table for printing"""
        self._rows.extend(rows)
        self.column_size(rows)

    @property
    def table_name(self) -> str:
        """Return table name"""
        return self._table_name

    @table_name.setter
    def table_name(self, table: str) -> None:
        """Set table name"""
        self._table_name = table

    @property
    def header(self) -> str:
        """Returns the title of the table"""
        return self._header

    @header.setter
    def header(self, header: str) -> None:
        """Returns the title of the table"""
        self._header = header
        self.column_size(header)

    def print_middle(self) -> str:
        """Returns table data as formatted strings"""
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
