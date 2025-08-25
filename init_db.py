import sqlite3
import os


def init_database():
    """Initialize the database with required tables if they don't exist."""
    # Ensure database directory exists
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect("database/data_source.db")
    cursor = conn.cursor()

    # Create user_details table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """
    )

    # Create syllabus table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS syllabus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            module_number TEXT,
            module_name TEXT,
            topic TEXT,
            inquiry_q TEXT,
            syllabus TEXT,
            confidence TEXT
        )
    """
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_database()
