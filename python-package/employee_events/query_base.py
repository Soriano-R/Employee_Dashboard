"""Abstract base class that shares queries between Employee and Team."""
from abc import ABC
from .sql_execution import QueryMixin, pandas_query

class QueryBase(QueryMixin, ABC):
    name: str = ""          # "employee" or "team" – set by subclass

    # ── names list (id + display_name) ───────────────────────────────────────
    @pandas_query
    def names(self):
        if self.name == "employee":
            return ("SELECT employee_id AS id, "
                    "first_name || ' ' || last_name AS display_name "
                    "FROM employee ORDER BY display_name")
        return ("SELECT team_id AS id, team_name AS display_name "
                "FROM team ORDER BY display_name")

    # ── generic note feed ────────────────────────────────────────────────────
    @pandas_query
    def notes(self, id_: int):
        id_col = f"{self.name}_id"
        return (f"SELECT note_date, note "
                f"FROM notes WHERE {id_col} = {id_} "
                f"ORDER BY note_date DESC")