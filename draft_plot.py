from support import request_header
import table as tb


class Border:
    def __init__(self):
        self.top_line = {"left": "╔", "right": "╗", "line": "═", "sep": "╦"}
        self.middle_line = {"left": "╠", "right": "╣", "line": "═", "sep": "╬"}
        self.bottom_line = {"left": "╚", "right": "╝", "line": "═", "sep": "╩"}
        # line: "─"
        self._row_separator = "║"  # "│"
        self.row = self.row_style(self._row_separator)
        self._column_size = list()

    def row_style(self, sep):
        return {
            "left": sep.ljust(2),
            "right": sep.rjust(2),
            "sep": sep.center(3),
        }

    def draw_line(self, line_style):
        draw = line_style["left"]
        draw += line_style["sep"].join(
            line_style["line"] * (column + 2) for column in self._column_size
        )
        draw += line_style["right"]
        return draw

    def draw_top(self):
        return self.draw_line(self.top_line)

    def draw_middle(self):
        return self.draw_line(self.middle_line)

    def draw_bottom(self):
        return self.draw_line(self.bottom_line)

    def draw_row(self, row):
        line = self.row["left"]
        line += self.row["sep"].join(self.align(row))
        line += self.row["right"]
        return line

    def align(self, row):
        for col, just in zip(row, self._column_size):
            yield str(col).center(just)

    @property
    def row_separator(self):
        return self._row_separator

    @row_separator.setter
    def row_separator(self, sep):
        self._row_separator = sep
        self.row = self.row_style(sep)


class Printify:
    def __init__(self, table="New_Table"):
        self._table_name = table
        self._header = tuple()
        self._column_size = list()
        self._rows = list()
        self._border = Border()

    def column_width(self, row):
        return list(map(len, map(str, row)))

    def columns_width(self, rows):
        return list(self.column_width(row) for row in rows)

    def max_columns_width(self, row):
        if type(row) == tuple:
            width = [self.column_width(row)]
        elif type(row) == list:
            width = self.columns_width(row)
        column_size = list(map(max, zip(*width, self._column_size)))
        self._border._column_size = column_size
        return column_size
      
    def column_size(self, row):
        if self._column_size == list():
            self._column_size = [0] * len(self._header)
        self._column_size = self.max_columns_width(row)

    def add_row(self, row):
        self._rows.append(row)
        self.column_size(row)

    def add_rows(self, rows):
        self._rows.extend(rows)
        self.column_size(rows)

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, table):
        self._table_name = table

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header
        self.column_size(header)
    
    def print_middle(self):
        sep = f"\n{self._border.draw_middle()}\n"
        data = [self._header, *self._rows]
        return f"\n{sep.join(self._border.draw_row(row) for row in data)}\n"

    def __str__(self):
        line = self._border.draw_top()
        line += self.print_middle()
        line += self._border.draw_bottom()
        line += f"\ntable '{self._table_name}'"
        return line


table = Printify("versus")
table.header = request_header(table.table_name)
table.add_rows(tb.read(table.table_name))
print(table)

table1 = Printify("win_loss")
table1.header = request_header(table1.table_name)
table1.add_rows(tb.read(table1.table_name))
print(table1)

table2 = Printify("overall")
table2.header = request_header(table2.table_name)
table2.add_rows(tb.read(table2.table_name))
print(table2)
