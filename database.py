import os

import mysql.connector


DEFAULT_DATABASE_NAME = "student5"
STUDENTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS students (
    student_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    student_name VARCHAR(120) NOT NULL,
    study_hours DECIMAL(5, 2) NOT NULL,
    attendance DECIMAL(5, 2) NOT NULL,
    previous_marks DECIMAL(5, 2) NOT NULL,
    assignment_score DECIMAL(5, 2) NOT NULL,
    sleep_hours DECIMAL(5, 2) NOT NULL,
    predicted_marks DECIMAL(6, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id),
    INDEX idx_students_created_at (created_at),
    INDEX idx_students_predicted_marks (predicted_marks)
)
"""

DATABASE_SETUP_MESSAGE = (
    "MySQL is unavailable. Configure DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, "
    "and DB_NAME, make sure the MySQL server is running, then run "
    "python database.py to initialize the database."
)


class DatabaseConfigurationError(Exception):
    pass


def _connection_options(include_database=True):
    try:
        port = int(os.getenv("DB_PORT", "3306"))
    except ValueError as error:
        raise DatabaseConfigurationError("DB_PORT must be a valid port number.") from error

    options = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": port,
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "connection_timeout": 5,
    }
    if include_database:
        options["database"] = os.getenv("DB_NAME", DEFAULT_DATABASE_NAME)
    return options


def get_db_connection():
    return mysql.connector.connect(**_connection_options())


def initialize_database():
    database_name = os.getenv("DB_NAME", DEFAULT_DATABASE_NAME)
    escaped_database_name = database_name.replace("`", "``")

    server_connection = mysql.connector.connect(**_connection_options(False))
    try:
        cursor = server_connection.cursor()
        try:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{escaped_database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        finally:
            cursor.close()
    finally:
        server_connection.close()

    database_connection = get_db_connection()
    try:
        cursor = database_connection.cursor()
        try:
            cursor.execute(STUDENTS_TABLE_SQL)
            database_connection.commit()
        except mysql.connector.Error:
            database_connection.rollback()
            raise
        finally:
            cursor.close()
    finally:
        database_connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database and students table are ready.")
