import sqlite3


DATABASE_PATH = "monitor.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            status_code TEXT NOT NULL,
            response_time_ms INTEGER NOT NULL,
            checked_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()
    
def save_check(result):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO checks (
            url,
            status,
            status_code,
            response_time_ms,
            checked_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            result["url"],
            result["status"],
            result["status_code"],
            result["response_time_ms"],
            result["checked_at"],
        ),
    )

    connection.commit()
    connection.close()