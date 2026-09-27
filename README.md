\# Personal Expense Tracker App



A modular Python web application built using \*\*Streamlit\*\*, \*\*SQLite3\*\*, and \*\*Plotly\*\* to record, analyze, and manage personal expenses safely and efficiently.



\## Features

\- \*\*Transaction Logging\*\*: Record date, category, amount, and notes.

\- \*\*Data Visualizations\*\*: Dynamic charts showing category-wise distribution and spending trends.

\- \*\*Robust Error Handling\*\*: Input validation and database exception safety.

\- \*\*Logging\*\*: Configured system logging to track activities in `logs/app.log`.

\- \*\*Database Persistence\*\*: SQLite storage engine.



\## Database Schema

\- `id`: INTEGER (PRIMARY KEY)

\- `date`: TEXT

\- `category`: TEXT

\- `amount`: REAL

\- `description`: TEXT

\- `created\_at`: TIMESTAMP



\## How to Run Locally

1\. Install dependencies: `pip install -r requirements.txt`

2\. Run app: `streamlit run app.py`

