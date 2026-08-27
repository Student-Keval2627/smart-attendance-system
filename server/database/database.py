import os
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient


load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "smart_attendance")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not configured. Add it to your local .env file "
        "and to Render Environment Variables."
    )

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client[MONGO_DB_NAME]


# ==================================================
# DATABASE HELPERS
# ==================================================

def get_db():
    return db


def get_db_connection():
    """Backward-compatible alias while the project moves from SQLite."""
    return db


def to_object_id(value):
    if isinstance(value, ObjectId):
        return value

    if not value:
        return None

    try:
        return ObjectId(str(value))
    except (InvalidId, TypeError):
        return None


def normalize_doc(document):
    """Convert MongoDB ObjectIds into template-friendly strings."""
    if not document:
        return None

    result = dict(document)

    if "_id" in result:
        result["id"] = str(result.pop("_id"))

    for key, value in list(result.items()):
        if isinstance(value, ObjectId):
            result[key] = str(value)

    return result


def normalize_docs(documents):
    return [normalize_doc(document) for document in documents]


def utc_now():
    return datetime.now(timezone.utc)


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

def init_db():
    """Verify MongoDB and create indexes used by the application."""
    client.admin.command("ping")

    db.teachers.create_index(
        [("username", ASCENDING)],
        unique=True,
        name="unique_teacher_username"
    )

    db.classes.create_index(
        [("teacher_id", ASCENDING)],
        name="classes_by_teacher"
    )

    db.students.create_index(
        [("class_id", ASCENDING), ("roll_no", ASCENDING)],
        unique=True,
        name="unique_roll_per_class"
    )

    db.attendance.create_index(
        [
            ("student_id", ASCENDING),
            ("class_id", ASCENDING),
            ("attendance_date", ASCENDING),
            ("attendance_type", ASCENDING)
        ],
        unique=True,
        name="unique_student_attendance_session"
    )

    db.attendance.create_index(
        [
            ("class_id", ASCENDING),
            ("attendance_date", ASCENDING),
            ("attendance_type", ASCENDING)
        ],
        name="attendance_history_lookup"
    )

    print(
        f"MongoDB connected successfully. Database: {MONGO_DB_NAME}"
    )


if __name__ == "__main__":
    init_db()
