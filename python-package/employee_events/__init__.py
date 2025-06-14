"""
Employee-Events utility package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exposes high-level query classes that handle all DB access.

Usage
-----
>>> from employee_events import Employee, Team
>>> Employee().event_counts(42)
"""
from .employee import Employee
from .team import Team
from .query_base import QueryBase   
from .sql_execution import *


__all__ = ["Employee", "Team", "QueryBase"]