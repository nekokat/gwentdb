from connection import CONN, CURSOR
import pivot as pv
from support import request_header


MASTER_TABLE = ("lastrow", "games")
PIVOT_TABLE = ("win_loss", "versus", "overall")


def table_header(table: str) -> str:
    """Creating table header for db query"""
    header = request_header(table)
    l = len(header)
    if table in MASTER_TABLE:
        types = ("TEXT",) * l
    elif table in ["win_loss", "versus"]:
        types = ("TEXT",) + ("INTEGER",) * (l - 1)
    elif table in ["overall"]:
        types = ("INTEGER",) * l
    title = [f'"{col}" {col_type}' for col, col_type in zip(header, types)]
    return "({})".format(", ".join(title))


def create(table: str) -> None:
    """Database query to create a table"""
    request = f"CREATE TABLE {table} {table_header(table)}"
    CURSOR.execute(request)
    CONN.commit()


def create_pivot(table: str) -> None:
    """Database query to create a pivot table"""
    create(table)
    pv.write(table)


def createall() -> None:
    """Creates all tables in the database."""
    for table in MASTER_TABLE:
        create(table)
    for table in PIVOT_TABLE:
        create_pivot(table)
