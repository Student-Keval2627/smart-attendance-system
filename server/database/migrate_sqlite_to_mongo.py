import os
import sqlite3
from datetime import datetime, timezone

from database import get_db, init_db


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(BASE_DIR, "attendance.db")
)


def migrate():
    if not os.path.exists(SQLITE_DB_PATH):
        raise FileNotFoundError(
            f"SQLite database not found: {SQLITE_DB_PATH}"
        )

    init_db()
    mongo = get_db()

    # Prevent accidental duplicate migration.
    if any(
        mongo[name].count_documents({}) > 0
        for name in ("teachers", "classes", "students", "attendance")
    ):
        raise RuntimeError(
            "MongoDB is not empty. Use an empty database for the first migration."
        )

    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row

    teacher_map = {}
    class_map = {}
    student_map = {}

    try:
        for row in conn.execute("SELECT * FROM teachers ORDER BY id"):
            result = mongo.teachers.insert_one({
                "username": row["username"],
                "password": row["password"],
                "name": row["name"] or "",
                "mobile": row["mobile"] or "",
                "age": row["age"],
                "qualification": row["qualification"] or "",
                "created_at": datetime.now(timezone.utc)
            })
            teacher_map[row["id"]] = result.inserted_id

        for row in conn.execute("SELECT * FROM classes ORDER BY id"):
            teacher_id = teacher_map.get(row["teacher_id"])
            if not teacher_id:
                continue

            result = mongo.classes.insert_one({
                "teacher_id": teacher_id,
                "class_name": row["class_name"],
                "batch": row["batch"],
                "created_at": datetime.now(timezone.utc)
            })
            class_map[row["id"]] = result.inserted_id

        for row in conn.execute("SELECT * FROM students ORDER BY id"):
            class_id = class_map.get(row["class_id"])
            if not class_id:
                continue

            result = mongo.students.insert_one({
                "class_id": class_id,
                "name": row["name"],
                "roll_no": row["roll_no"],
                "mobile": row["mobile"] or "",
                "created_at": datetime.now(timezone.utc)
            })
            student_map[row["id"]] = result.inserted_id

        for row in conn.execute("SELECT * FROM attendance ORDER BY id"):
            student_id = student_map.get(row["student_id"])
            class_id = class_map.get(row["class_id"])
            teacher_id = teacher_map.get(row["teacher_id"])

            if not student_id or not class_id or not teacher_id:
                continue

            mongo.attendance.insert_one({
                "student_id": student_id,
                "class_id": class_id,
                "teacher_id": teacher_id,
                "attendance_date": row["attendance_date"],
                "attendance_type": "Theory",
                "status": row["status"],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            })

    finally:
        conn.close()

    print("Migration completed successfully.")
    print("Legacy attendance was imported as Theory attendance.")
    print("Teachers:", mongo.teachers.count_documents({}))
    print("Classes:", mongo.classes.count_documents({}))
    print("Students:", mongo.students.count_documents({}))
    print("Attendance records:", mongo.attendance.count_documents({}))


if __name__ == "__main__":
    migrate()
