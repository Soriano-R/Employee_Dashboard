"""
FastHTML dashboard for monitoring employee / team performance
and predicted recruitment risk.
Run locally with:
    uvicorn report.dashboard:app --reload
"""
from fasthtml import FastHTML, h
from fasthtml.components import (Dropdown, Card, DataTable,
                                 FormGroup, MatplotlibViz)
import matplotlib.pyplot as plt
import pandas as pd

# business logic
from employee_events import Employee, Team
from report.utils import load_model

# ──────────────────────────────────────────────────────────────
# Reusable FastHTML components
# ──────────────────────────────────────────────────────────────
class DashboardFilters(FormGroup):
    """Profile type selector + dynamic name list."""

    def __init__(self):
        super().__init__()
        self.profile_type = Dropdown(values=["Employee", "Team"],
                                     placeholder="Profile Type")
        self.name_select  = Dropdown(placeholder="Select…")
        self.children     = [self.profile_type, self.name_select]

    def refresh_names(self):
        """Populate second dropdown based on first selection."""
        if self.profile_type.value == "Employee":
            df = Employee().names()
        elif self.profile_type.value == "Team":
            df = Team().names()
        else:
            df = pd.DataFrame([])
        self.name_select.values = df["display_name"].tolist()
        self.name_select.meta   = df.set_index("display_name")["id"].to_dict()


class EventTrend(MatplotlibViz):
    """Line plot of + / – events over time."""

    def visualization(self, model, asset_id, **_):
        df = model.event_counts(asset_id)
        fig, ax = plt.subplots()
        ax.plot(df["event_date"], df["positive_events"], label="Positive")
        ax.plot(df["event_date"], df["negative_events"], label="Negative")
        ax.set_title("Daily Performance Events")
        ax.legend()
        fig.autofmt_xdate()
        return fig


class RiskCard(Card):
    """Displays mean probability of recruitment."""

    predictor = load_model()

    def __init__(self, model, asset_id):
        prob = self._probability(model, asset_id)
        super().__init__(title="Recruitment Risk",
                         children=[h.h2(f"{prob:.1%}")])

    def _probability(self, model, asset_id):
        df = model.model_data(asset_id)
        proba = self.predictor.predict_proba(df)[:, 1]
        return float(proba.mean())


# ──────────────────────────────────────────────────────────────
# FastHTML application + routes
# ──────────────────────────────────────────────────────────────
app = FastHTML()                 # Uvicorn entry-point: report.dashboard:app
filters = DashboardFilters()     # single instance used on index & sub-pages


@app.route("/")
def index():
    """Landing page with just the filter widget."""
    filters.refresh_names()
    return h.section(filters)


@app.route("/employee/{employee_id}")
def employee(employee_id: int):
    emp = Employee()
    filters.profile_type.value = "Employee"
    filters.refresh_names()
    main = h.section(
        filters,
        RiskCard(emp, employee_id),
        EventTrend(emp, employee_id)
    )
    return main


@app.route("/team/{team_id}")
def team(team_id: int):
    tm = Team()
    filters.profile_type.value = "Team"
    filters.refresh_names()
    main = h.section(
        filters,
        RiskCard(tm, team_id),
        EventTrend(tm, team_id)
    )
    return main