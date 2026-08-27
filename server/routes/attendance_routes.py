from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database.database import get_db, normalize_doc, to_object_id, utc_now


attendance_bp = Blueprint("attendance", __name__)
ATTENDANCE_TYPES = ("Theory", "Practical", "Tutorial")


def _get_owned_class(class_id, teacher_id):
    class_oid = to_object_id(class_id)
    teacher_oid = to_object_id(teacher_id)

    if not class_oid or not teacher_oid:
        return None, None, None

    db = get_db()
    class_doc = db.classes.find_one({
        "_id": class_oid,
        "teacher_id": teacher_oid
    })

    return class_oid, teacher_oid, class_doc


@attendance_bp.route(
    "/class/<class_id>/collect-attendance",
    methods=["GET", "POST"]
)
def collect_attendance(class_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    class_oid, teacher_oid, class_doc = _get_owned_class(
        class_id,
        session["teacher_id"]
    )

    if not class_doc:
        return "Class not found", 404

    db = get_db()
    teacher_doc = db.teachers.find_one({"_id": teacher_oid})

    if request.method == "POST":
        attendance_date = request.form.get("attendance_date", "").strip()
        attendance_type = request.form.get("attendance_type", "").strip()

        if attendance_type not in ATTENDANCE_TYPES:
            flash("Please select Theory, Practical or Tutorial.")
            return redirect(url_for("attendance.collect_attendance", class_id=class_id))

        if not attendance_date:
            flash("Please select attendance date.")
            return redirect(url_for("attendance.collect_attendance", class_id=class_id))

        try:
            selected_date = datetime.strptime(attendance_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid attendance date.")
            return redirect(url_for("attendance.collect_attendance", class_id=class_id))

        if selected_date > date.today():
            flash("Future date attendance is not allowed.")
            return redirect(url_for("attendance.collect_attendance", class_id=class_id))

        session["attendance_date"] = attendance_date
        session["attendance_class_id"] = class_id
        session["attendance_type"] = attendance_type

        return redirect(url_for("attendance.mark_attendance", class_id=class_id))

    return render_template(
        "collect_attendance.html",
        class_info=normalize_doc(class_doc),
        teacher=normalize_doc(teacher_doc),
        today=date.today().isoformat(),
        attendance_types=ATTENDANCE_TYPES
    )


@attendance_bp.route(
    "/class/<class_id>/mark-attendance",
    methods=["GET", "POST"]
)
def mark_attendance(class_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    attendance_date = session.get("attendance_date")
    attendance_class_id = session.get("attendance_class_id")
    attendance_type = session.get("attendance_type")

    if (
        not attendance_date
        or attendance_class_id != class_id
        or attendance_type not in ATTENDANCE_TYPES
    ):
        session.pop("attendance_date", None)
        session.pop("attendance_class_id", None)
        session.pop("attendance_type", None)
        return redirect(url_for("attendance.collect_attendance", class_id=class_id))

    class_oid, teacher_oid, class_doc = _get_owned_class(
        class_id,
        session["teacher_id"]
    )

    if not class_doc:
        return "Class not found", 404

    db = get_db()
    teacher_doc = db.teachers.find_one({"_id": teacher_oid})
    student_docs = list(db.students.find({"class_id": class_oid}).sort("roll_no", 1))

    students = []
    for student_doc in student_docs:
        student_oid = student_doc["_id"]

        total = db.attendance.count_documents({
            "student_id": student_oid,
            "class_id": class_oid,
            "attendance_type": attendance_type
        })

        present = db.attendance.count_documents({
            "student_id": student_oid,
            "class_id": class_oid,
            "attendance_type": attendance_type,
            "status": "Present"
        })

        current = db.attendance.find_one({
            "student_id": student_oid,
            "class_id": class_oid,
            "attendance_date": attendance_date,
            "attendance_type": attendance_type
        })

        student = normalize_doc(student_doc)
        student["attendance_percentage"] = round((present / total) * 100, 1) if total else 0
        student["current_status"] = current.get("status") if current else None
        students.append(student)

    if request.method == "POST":
        if not students:
            flash("No students found in this class.")
            return redirect(url_for("class_routes.open_class", class_id=class_id))

        present_students = set(request.form.getlist("present_students"))

        try:
            for student_doc in student_docs:
                student_id_text = str(student_doc["_id"])
                status = "Present" if student_id_text in present_students else "Absent"

                db.attendance.update_one(
                    {
                        "student_id": student_doc["_id"],
                        "class_id": class_oid,
                        "attendance_date": attendance_date,
                        "attendance_type": attendance_type
                    },
                    {
                        "$set": {
                            "teacher_id": teacher_oid,
                            "status": status,
                            "updated_at": utc_now()
                        },
                        "$setOnInsert": {
                            "created_at": utc_now()
                        }
                    },
                    upsert=True
                )
        except Exception as exc:
            print("Attendance save error:", exc)
            flash("Unable to save attendance. Please try again.")
            return redirect(url_for("attendance.mark_attendance", class_id=class_id))

        session.pop("attendance_date", None)
        session.pop("attendance_class_id", None)
        session.pop("attendance_type", None)

        flash(f"{attendance_type} attendance submitted successfully!")
        return redirect(url_for("class_routes.open_class", class_id=class_id))

    return render_template(
        "mark_attendance.html",
        class_info=normalize_doc(class_doc),
        teacher=normalize_doc(teacher_doc),
        students=students,
        attendance_date=attendance_date,
        attendance_type=attendance_type
    )


@attendance_bp.route("/class/<class_id>/attendance-history")
def attendance_history(class_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    class_oid, teacher_oid, class_doc = _get_owned_class(
        class_id,
        session["teacher_id"]
    )

    if not class_doc:
        return "Class not found", 404

    pipeline = [
        {
            "$match": {
                "class_id": class_oid,
                "teacher_id": teacher_oid
            }
        },
        {
            "$group": {
                "_id": {
                    "attendance_date": "$attendance_date",
                    "attendance_type": "$attendance_type"
                },
                "present_count": {
                    "$sum": {"$cond": [{"$eq": ["$status", "Present"]}, 1, 0]}
                },
                "absent_count": {
                    "$sum": {"$cond": [{"$eq": ["$status", "Absent"]}, 1, 0]}
                },
                "total_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.attendance_date": -1, "_id.attendance_type": 1}}
    ]

    history = []
    for item in get_db().attendance.aggregate(pipeline):
        history.append({
            "attendance_date": item["_id"]["attendance_date"],
            "attendance_type": item["_id"].get("attendance_type", "Theory"),
            "present_count": item["present_count"],
            "absent_count": item["absent_count"],
            "total_count": item["total_count"]
        })

    return render_template(
        "attendance_history.html",
        class_info=normalize_doc(class_doc),
        history=history
    )


@attendance_bp.route(
    "/class/<class_id>/attendance-history/<attendance_date>/<attendance_type>"
)
def view_attendance_date(class_id, attendance_date, attendance_type):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    if attendance_type not in ATTENDANCE_TYPES:
        return "Invalid attendance type", 404

    try:
        datetime.strptime(attendance_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid attendance date", 404

    class_oid, teacher_oid, class_doc = _get_owned_class(
        class_id,
        session["teacher_id"]
    )

    if not class_doc:
        return "Class not found", 404

    db = get_db()
    records = list(
        db.attendance.find({
            "class_id": class_oid,
            "teacher_id": teacher_oid,
            "attendance_date": attendance_date,
            "attendance_type": attendance_type
        })
    )

    attendance_records = []
    for record in records:
        student_doc = db.students.find_one({"_id": record["student_id"]})
        if not student_doc:
            continue

        attendance_records.append({
            "name": student_doc.get("name", ""),
            "roll_no": student_doc.get("roll_no", ""),
            "status": record.get("status", "Absent")
        })

    attendance_records.sort(key=lambda student: str(student["roll_no"]))

    return render_template(
        "attendance_date_view.html",
        class_info=normalize_doc(class_doc),
        attendance_records=attendance_records,
        attendance_date=attendance_date,
        attendance_type=attendance_type
    )
