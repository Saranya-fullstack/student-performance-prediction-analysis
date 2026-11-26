import math
import os
from pathlib import Path

import joblib
import mysql.connector
import pandas as pd
from flask import Flask, jsonify, render_template, request

from database import DATABASE_SETUP_MESSAGE, DatabaseConfigurationError, get_db_connection

app = Flask(__name__, template_folder="template")
project_dir = Path(__file__).resolve().parent
model = joblib.load(project_dir / "models" / "random_forest_regression.joblib")
FEATURES = {
    "study_hours": (0, 24),
    "attendance": (0, 100),
    "previous_marks": (0, 100),
    "assignment_score": (0, 100),
    "sleep_hours": (0, 24),
}


def fetch_all(query, parameters=()):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, parameters)
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


def save_student(student_name, values, prediction):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO students (
                    student_name, study_hours, attendance, previous_marks,
                    assignment_score, sleep_hours, predicted_marks
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (student_name, *values, prediction),
            )
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error:
            connection.rollback()
            raise
        finally:
            cursor.close()
    finally:
        connection.close()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/predict")
def prediction_form():
    return render_template("predict.html")


@app.get("/dashboard")
def dashboard():
    try:
        stats = fetch_all(
            """
            SELECT COUNT(*) AS total_students,
                   COALESCE(AVG(predicted_marks), 0) AS average_marks,
                   COALESCE(MAX(predicted_marks), 0) AS highest_marks,
                   COALESCE(
                       100.0 * SUM(predicted_marks >= 40) / NULLIF(COUNT(*), 0),
                       0
                   ) AS pass_percentage
            FROM students
            """
        )[0]
        recent_students = fetch_all(
            """
            SELECT student_name, predicted_marks
            FROM students
            ORDER BY created_at DESC, student_id DESC
            LIMIT 10
            """
        )
        distribution = fetch_all(
            """
            SELECT CASE
                       WHEN predicted_marks >= 85 THEN 'Excellent'
                       WHEN predicted_marks >= 70 THEN 'Good'
                       WHEN predicted_marks >= 50 THEN 'Average'
                       ELSE 'Needs Improvement'
                   END AS category,
                   COUNT(*) AS student_count
            FROM students
            GROUP BY category
            """
        )
        recent_students = [
            {
                **student,
                "predicted_marks": float(student["predicted_marks"]),
            }
            for student in recent_students
        ]
    except (mysql.connector.Error, DatabaseConfigurationError) as error:
        app.logger.warning(
            "Could not load dashboard analytics from MySQL; using the included dataset: %s",
            error,
        )
        sample_data = pd.read_csv(project_dir / "src" / "dataset" / "student_data.csv")
        marks = sample_data["final_marks"]
        stats = {
            "total_students": len(sample_data),
            "average_marks": float(marks.mean()),
            "highest_marks": float(marks.max()),
            "pass_percentage": float((marks >= 40).mean() * 100),
        }
        recent_students = [
            {
                "student_name": f"Student {int(row.student_id)}",
                "predicted_marks": float(row.final_marks),
            }
            for row in sample_data.tail(10).itertuples()
        ]
        categories = (
            ("Excellent", marks >= 85),
            ("Good", (marks >= 70) & (marks < 85)),
            ("Average", (marks >= 50) & (marks < 70)),
            ("Needs Improvement", marks < 50),
        )
        distribution = [
            {"category": category, "student_count": int(mask.sum())}
            for category, mask in categories
            if mask.any()
        ]
        return render_template(
            "dashboard.html",
            total_students=stats["total_students"],
            average_marks=round(stats["average_marks"], 2),
            highest_marks=round(stats["highest_marks"], 2),
            pass_percentage=round(stats["pass_percentage"], 2),
            recent_students=recent_students,
            distribution=distribution,
            data_source_message=(
                "MySQL is unavailable. Showing sample analytics from the included "
                "training dataset; saved prediction records are not included."
            ),
        )

    return render_template(
        "dashboard.html",
        total_students=stats["total_students"],
        average_marks=round(float(stats["average_marks"]), 2),
        highest_marks=round(float(stats["highest_marks"]), 2),
        pass_percentage=round(float(stats["pass_percentage"]), 2),
        recent_students=recent_students,
        distribution=distribution,
    )


@app.get("/students")
def students():
    try:
        student_records = fetch_all(
            """
            SELECT student_id, student_name, study_hours, attendance,
                   previous_marks, assignment_score, sleep_hours,
                   predicted_marks, created_at
            FROM students
            ORDER BY created_at DESC, student_id DESC
            """
        )
    except (mysql.connector.Error, DatabaseConfigurationError):
        app.logger.exception("Could not load student records from MySQL.")
        return render_template(
            "student.html",
            students=[],
            database_error=DATABASE_SETUP_MESSAGE,
        ), 503
    return render_template("student.html", students=student_records)


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Prediction data must be a JSON object."), 400

    student_name = data.get("student_name", "Unnamed student")
    if not isinstance(student_name, str) or not student_name.strip():
        return jsonify(error="student_name must not be empty."), 400
    student_name = student_name.strip()
    if len(student_name) > 120:
        return jsonify(error="student_name must be 120 characters or fewer."), 400

    values = []
    for feature, (minimum, maximum) in FEATURES.items():
        value = data.get(feature)
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not minimum <= value <= maximum
            or not math.isfinite(value)
        ):
            return jsonify(
                error=f"{feature} must be a number from {minimum} to {maximum}."
            ), 400
        values.append(float(value))

    student = pd.DataFrame([values], columns=FEATURES)
    prediction = float(model.predict(student)[0])
    try:
        student_id = save_student(student_name, values, prediction)
    except (mysql.connector.Error, DatabaseConfigurationError):
        app.logger.exception("Prediction succeeded, but saving it to MySQL failed.")
        return jsonify(
            student_name=student_name,
            prediction=prediction,
            saved=False,
            warning=f"Prediction calculated, but it was not saved. {DATABASE_SETUP_MESSAGE}",
        )

    return jsonify(
        student_id=student_id,
        student_name=student_name,
        prediction=prediction,
        saved=True,
    )


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", use_reloader=False)
