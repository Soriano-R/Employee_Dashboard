# Employee Performance Dashboard

This project implements an interactive web-based dashboard for exploring employee performance events. It allows filtering employees by team, viewing individual performance charts, and inspecting recent manager notes.

The dashboard uses FastHTML for building HTML components directly in Python, and SQLite for persistent data storage.

## Features

- List employees with 4-digit IDs
- Filter employees by team using a dropdown
- Navigate to individual employee detail pages
- View performance charts showing positive and negative events over time
- Display recent manager notes
- Back to Main Page button on detail views
- Colorblind-friendly plots
- Fully responsive and minimal design

## Correct Repository Structure

Your project directory should look like this before pushing to GitHub:
```
Employee_Dashboard/
├── assets/
│   ├── report.css
│   └── chart_<uuid>.png        # Generated performance charts
├── python-package/
│   └── employee_events/
│       ├── __init__.py, employee.py, ...
│       └── employee_events.db  # SQLite database
├── report/
│   ├── dashboard.py
│   └── templates/
│       ├── index.html
│       └── detail.html
├── requirements.txt
├── README.md
└── ...
```
This structure ensures your repo shows all directories correctly on GitHub.

## Installation

Create and activate a Python virtual environment:

python -m venv dashboard_env
source dashboard_env/bin/activate  # macOS/Linux
# or
dashboard_env\Scripts\activate     # Windows

Install required packages:

pip install -r requirements.txt

## Running the Dashboard

Start the FastHTML server via Uvicorn:

python -m uvicorn report.dashboard:app --reload

Then visit http://127.0.0.1:8000 in your web browser.

## Data

Employee and team information comes from the SQLite database at python-package/employee_events/employee_events.db, which includes:

- employee table: employee IDs, names, and team assignments.
- team table: team IDs, names, and manager names.
- employee_events table: historical positive and negative events for each employee.
- notes table: recent manager comments on employee performance.

The dashboard queries this database to dynamically populate employee lists, team filters, and individual charts.

## Charts

Performance charts are generated with Matplotlib using colorblind-friendly color schemes (#0072B2 for positive events, #D55E00 for negative events). Charts show monthly event counts with date axes formatted for readability.

## Filtering

On the main page:
- Select a team from the dropdown to filter employees.
- Select All Teams to show every employee.

## Navigation

- Click an employee entry to view details, including performance trends and manager notes.
- Use the Back to Main Page link (top-right of detail pages) to return to the employee list.

## Notes

- Adjust report/dashboard.py if your database file or schema changes.
- The dashboard assumes employee event data is up-to-date in the SQLite database.

## Project Inspiration

This dashboard design was inspired in part by the [Udacity Data Science Dashboard Project](https://github.com/udacity/dsnd-dashboard-project). Concepts of interactive dashboards, employee-centric visualizations, and performance reporting informed the design and implementation of this project.

To obtain the Udacity example project locally for reference, run:

```
git clone https://github.com/udacity/dsnd-dashboard-project.git
cd dsnd-dashboard-project
```

You can then inspect their code and compare it with this implementation to see how different approaches to dashboarding are built.

## Authors

Developed as part of a data science capstone project.

## License

This project is licensed under the MIT License — see the LICENSE.txt file for details.
