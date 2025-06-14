"""Pytest smoke-tests for DB existence & core tables."""
import sqlite3
from pathlib import Path
import pytest

project_root = Path(__file__).resolve().parent.parent
db_path      = project_root / "python-package" / "employee_events" / "employee_events.db"

# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def db_conn():
    return sqlite3.connect(db_path)

@pytest.fixture(scope="session")
def tables(db_conn):
    rows = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return {r[0] for r in rows}

# ---------------------------------------------------------------------------
def test_db_exists():
    assert db_path.exists()

def test_employee_table_exists(tables):
    assert "employee" in tables

def test_team_table_exists(tables):
    assert "team" in tables

def test_employee_events_table_exists(tables):
    assert "employee_events" in tables