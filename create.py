import pivot as pv
from sql import Query

q = Query()


def create(table: str) -> None:
    """Database query to create a table"""
    q.create(table).execute().commit()


def create_pivot(table: str) -> None:
    """Database query to create a pivot table"""
    create(table)
    pv.write(table)


def create_all() -> None:
    """Creates all tables in the database."""
    for table in ("lastrow", "games"):
        create(table)
    for table in ("win_loss", "versus", "overall"):
        create_pivot(table)
