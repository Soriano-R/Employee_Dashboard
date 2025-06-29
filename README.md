# Employee Performance Dashboard

This project implements an interactive web-based dashboard for exploring employee performance events. It allows filtering employees by team, viewing individual performance charts, and inspecting recent manager notes.

The dashboard uses FastHTML for building HTML components directly in Python, and SQLite for persistent data storage.

## 🎥 Application Demo

[![Watch the Demo](https://img.shields.io/badge/Video-Demo-blue)](https://app.screencast.com/DGQPc0bQ2dgfC)

## 📸 Application Screenshots

### Home Page
![Dashboard Home](https://github.com/Soriano-R/Employee_Dashboard/blob/main/docs/dashboard_home.png)

### Employee Detail Page
![Employee Detail](https://github.com/Soriano-R/Employee_Dashboard/blob/main/docs/employee_detail.png)

## What Was Done

- **Database Creation**: Built a normalized SQLite database containing tables for employees, teams, events, and manager notes. Populated with synthetic data for demonstration.
- **Object-Oriented Design**: Implemented Employee and Team classes to abstract data access.
- **Dashboard Layout**: Designed an employee list page with team filter dropdown, styled with basic CSS, and employee detail pages with charts.
- **Event Charting**: Created colorblind-friendly bar charts using Matplotlib showing monthly positive and negative events for employees.
- **Routing & Templates**: Developed routes for the main page and detail pages using FastAPI and Jinja2 templates.
- **Filter Functionality**: Added dropdown to filter employees by team; when 'All Teams' is selected, all employees are shown.
- **Navigation**: Added a Back to Main Page link at the top-right corner of employee detail pages.
- **Readability Improvements**: Reformatted date axes on charts, displayed employee IDs in 4-digit format, and styled UI for a clean, corporate look.

## Repository Structure
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

## Cloning and Running the Dashboard

To clone this dashboard project and run it locally, execute:

```
git clone https://github.com/Soriano-R/Employee_Dashboard.git
cd Employee_Dashboard
```

Then create and activate a virtual environment:

python -m venv dashboard_env
source dashboard_env/bin/activate  # macOS/Linux
# or
dashboard_env\Scripts\activate     # Windows

Install required packages:

pip install -r requirements.txt

Finally, run the dashboard server:

python -m uvicorn report.dashboard:app --reload

Visit http://127.0.0.1:8000 in your browser.

## Data

Employee and team information comes from the SQLite database at python-package/employee_events/employee_events.db, which includes:

- employee table: employee IDs, names, and team assignments.
- team table: team IDs, names, and manager names.
- employee_events table: historical positive and negative events for each employee.
- notes table: recent manager comments on employee performance.

## Charts

Performance charts are generated with Matplotlib using colorblind-friendly color schemes (#0072B2 for positive events, #D55E00 for negative events). Charts show monthly event counts with date axes formatted for readability.

## Filtering

On the main page:
- Select a team from the dropdown to filter employees.
- Select All Teams to show every employee.

## Navigation

- Click an employee entry to view details, including performance trends and manager notes.
- Use the Back to Main Page link (top-right of detail pages) to return to the employee list.

## Project Inspiration

This dashboard design was inspired in part by the [Udacity Data Science Dashboard Project](https://github.com/udacity/dsnd-dashboard-project). Concepts of interactive dashboards, employee-centric visualizations, and performance reporting informed the design and implementation of this project.

To obtain the Udacity example project locally for reference, run:

```
git clone https://github.com/udacity/dsnd-dashboard-project.git
cd dsnd-dashboard-project
```

You can then inspect their code and compare it with this implementation to see how different approaches to dashboarding are built.

## Authors

Developed as part of a data science project.

## License

This project is licensed under the MIT License — see the LICENSE.txt file for details.
