"""Queries specific to a team."""
from .query_base import QueryBase
from .sql_execution import pandas_query

class Team(QueryBase):
    name = "team"

    @pandas_query
    def event_counts(self, team_id: int):
        return ("SELECT event_date, "
                "       SUM(positive_events) AS positive_events, "
                "       SUM(negative_events) AS negative_events "
                "FROM employee_events "
                f"WHERE team_id = {team_id} "
                "GROUP BY event_date ORDER BY event_date")

    @pandas_query
    def model_data(self, team_id: int):
        return ("SELECT employee_id, "
                "       SUM(positive_events) AS positive_events, "
                "       SUM(negative_events) AS negative_events "
                "FROM employee_events "
                f"WHERE team_id = {team_id} "
                "GROUP BY employee_id")

    @pandas_query
    def team_name(self, team_id: int):
        return f"SELECT team_name FROM team WHERE team_id = {team_id}"