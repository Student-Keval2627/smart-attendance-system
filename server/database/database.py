import os
import sqlite3


# ==================================================
# DATABASE PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "attendance.db"
)

SCHEMA_PATH = os.path.join(
    BASE_DIR,
    "schema.sql"
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_db_connection():

    conn = sqlite3.connect(
        DB_PATH
    )

    # Allow access like:
    # row["name"] instead of row[0]
    conn.row_factory = sqlite3.Row

    # Enable foreign key constraints
    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# ==================================================
# INITIALIZE DATABASE
# ==================================================

def init_db():

    print("Starting database setup...")

    conn = get_db_connection()

    try:

        with open(
            SCHEMA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            schema = file.read()

        conn.executescript(schema)

        conn.commit()

    except Exception as e:

        conn.rollback()

        print(
            "Database setup error:",
            e
        )

        raise

    finally:

        conn.close()

    print("Database setup completed successfully.")
    print("Database location:", DB_PATH)


# ==================================================
# RUN DATABASE SETUP DIRECTLY
# ==================================================

if __name__ == "__main__":

    init_db()