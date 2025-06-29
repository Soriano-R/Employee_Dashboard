"""Queries specific to a single employee."""
from .query_base import QueryBase
from .sql_execution import pandas_query

class Employee(QueryBase):
    name = "employee"

    @pandas_query
    def event_counts(self, employee_id: int):
        return ("SELECT event_date, positive_events, negative_events "
                "FROM employee_events "
                f"WHERE employee_id = {employee_id} "
                "ORDER BY event_date")

    @pandas_query
    def model_data(self, employee_id: int):
        return ("SELECT SUM(positive_events)  AS positive_events, "
                "       SUM(negative_events)  AS negative_events "
                "FROM employee_events "
                f"WHERE employee_id = {employee_id}")

    @pandas_query
    def full_name(self, employee_id: int):
        return (
            "SELECT first_name || ' ' || last_name AS full_name "
            f"FROM employee WHERE employee_id = {employee_id}"
        )

    @pandas_query
    def names(self):
        return (
            "SELECT employee_id, first_name || ' ' || last_name AS name "
            "FROM employee ORDER BY name"
        )