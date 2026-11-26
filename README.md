# Student- Performance- Prediction-analysis

A Flask application that predicts student marks with a trained Random Forest
regressor, saves prediction records in MySQL, and displays live student and
dashboard analytics.

## Requirements

- Python 3.10 or later
- MySQL 8.0 or later

## Setup

From the project directory, create and activate a virtual environment, then
install the Python dependencies:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the MySQL connection settings in the same PowerShell session. The defaults
are host `127.0.0.1`, port `3306`, user `root`, an empty password, and database
`student5`.

```powershell
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-mysql-password"
$env:DB_NAME = "student_performance_db"
```

Make sure the MySQL server is running, then create the database and students
table using the project connection settings:

```powershell
python .\database.py
```

The script creates the database and `students` table required by the app.

Start the application:

```powershell
python app.py
```

Open `http://127.0.0.1:5000`. Predictions submitted on the Predict page are
stored in MySQL and appear on the Students and Dashboard pages. Database-backed
pages report a service-unavailable error until MySQL is running, the schema has
been applied, and the connection settings are correct. If MySQL is unavailable,
the dashboard displays analytics from the included training dataset and labels
them as sample data.

## Project features

- Flask pages and JSON prediction API
- Student input validation and saved prediction history
- Responsive HTML and custom CSS with Bootstrap styling
- MySQL-backed student records and dashboard metrics/charts
- Existing training dataset, analysis notebook, and trained model artifacts
