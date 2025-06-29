from fasthtml.common import *
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Headless backend for server environments
import matplotlib.pyplot as plt
import numpy as np
import uuid
import sqlite3

app, route = fast_app()

# -- Database functions --
def get_employees():
    conn = sqlite3.connect("python-package/employee_events/employee_events.db")
    query = """
        SELECT e.employee_id AS id, e.first_name || ' ' || e.last_name AS name, t.team_name
        FROM employee e
        JOIN team t ON e.team_id = t.team_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_employee_detail(employee_id):
    conn = sqlite3.connect("python-package/employee_events/employee_events.db")
    detail = pd.read_sql(f"""
        SELECT e.employee_id, e.first_name || ' ' || e.last_name AS name,
               t.team_name, t.manager_name
        FROM employee e
        JOIN team t ON e.team_id = t.team_id
        WHERE e.employee_id = {employee_id}
    """, conn)
    events = pd.read_sql(f"""
        SELECT event_date, positive_events, negative_events
        FROM employee_events
        WHERE employee_id = {employee_id}
    """, conn, parse_dates=["event_date"])
    notes = pd.read_sql(f"""
        SELECT note, note_date
        FROM notes
        WHERE employee_id = {employee_id}
        ORDER BY note_date DESC
        LIMIT 5
    """, conn)
    conn.close()
    return detail.iloc[0], events, notes

# -- Routes --
@route("/")
def index(req):
    all_df = get_employees()
    teams = sorted(all_df["team_name"].unique())

    team_filter = req.query_params.get("team")
    if team_filter is not None:
        team_filter = team_filter.strip()

    # Updated filtering logic: show all employees if "All Teams" is selected or team_filter is None
    if team_filter and team_filter != "All Teams":
        df = all_df[all_df["team_name"] == team_filter]
    else:
        df = all_df

    # Dropdown options, send "All Teams" string so URL has team=All+Teams
    team_options = [
        Option("All Teams", value="All Teams", selected=(team_filter == "All Teams" or team_filter is None)),
    ] + [
        Option(team, value=team, selected=(team == team_filter)) for team in teams
    ]

    filter_dropdown = Form(
        Select(
            *team_options,
            name="team",
            _style="background-color:#888;padding:8px;border-radius:4px;",
            _onchange="this.form.submit()",
        ),
        action="/",
        method="get",
    )

    items = [
        Li(
            A(f"{row['id']:04d} - {row['name']}", href=f"/employee/{row['id']}")
        )
        for _, row in df.iterrows()
    ]

    return Section(
        H1("Select an Employee or Team"),
        filter_dropdown,
        Ul(*items) if items else P("No employees found for the selected team.")
    )

@route("/employee/{employee_id}")
def employee_detail(req, employee_id: int):
    detail, events, notes = get_employee_detail(employee_id)
    chart_path = generate_chart(events)
    return Section(
        Div(
            A("Back to Main Page", href="/", _style=(
                "position:absolute;top:20px;right:20px;"
                "font-size:20px;font-weight:bold;color:#0072B2;text-decoration:none;"
            )),
            _style="position:relative;"
        ),
        H1("Employee Performance"),
        H2(f"{detail['name']} (ID: {detail['employee_id']:04d})"),
        H2(f"Team: {detail['team_name']}"),
        H2(f"Manager: {detail['manager_name']}"),
        Img(src=chart_path, alt="Performance Chart") if chart_path else P("No events data."),
        H2("Recent Notes"),
        Ul(*[
            Li(f"{pd.to_datetime(row['note_date']).strftime('%Y-%m-%d')}: {row['note']}")
            for _, row in notes.iterrows()
        ]) if not notes.empty else P("No recent notes found."),
    )

# -- Chart generation --
def generate_chart(events_df):
    if events_df.empty:
        return ""
    events_df["event_date"] = pd.to_datetime(events_df["event_date"])
    monthly = events_df.resample("M", on="event_date").sum()
    monthly.index = monthly.index.strftime("%Y-%m")

    fig, ax = plt.subplots(figsize=(10, 5))
    monthly[["positive_events", "negative_events"]].plot.bar(ax=ax, color=["#0072B2", "#D55E00"])
    ax.set_title("Monthly Performance Events")
    ax.set_ylabel("Event Count")
    ax.set_xlabel("Month")
    fig.tight_layout()
    filename = f"assets/chart_{uuid.uuid4().hex}.png"
    fig.savefig(filename, bbox_inches="tight")
    plt.close(fig)
    return "/" + filename

serve()