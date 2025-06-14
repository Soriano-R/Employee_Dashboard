"""Generic helpers for talking to the local SQLite database."""
from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Absolute location of employee_events.db (…/employee_events/employee_events.db)
db_path = Path(__file__).resolve().parent / "employee_events.db"


# ─────────────────────────────────────────────────────────────────────────────
# M I X I N   (primary mechanism used by QueryBase / Employee / Team)
# ─────────────────────────────────────────────────────────────────────────────
class QueryMixin:
    """Reusable DB helpers for subclasses."""

    @staticmethod
    def _open():
        return connect(db_path)

    # Public helpers ----------------------------------------------------------
    def query(self, sql: str):
        """Return a list-of-tuples result set."""
        with self._open() as conn:
            return conn.execute(sql).fetchall()

    def pandas_query(self, sql: str):
        """Return a Pandas DataFrame."""
        with self._open() as conn:
            return pd.read_sql_query(sql, conn)


# ─────────────────────────────────────────────────────────────────────────────
# D E C O R A T O R S   (handy for one-liner query functions)
# ─────────────────────────────────────────────────────────────────────────────
def query(func):
    """Wraps a function that *returns* an SQL string → list-of-tuples."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        sql = func(*args, **kwargs)
        with connect(db_path) as conn:
            return conn.execute(sql).fetchall()

    return wrapper


def pandas_query(func):
    """Wraps a function that *returns* an SQL string → DataFrame."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        sql = func(*args, **kwargs)
        with connect(db_path) as conn:
            return pd.read_sql_query(sql, conn)

    return wrapper