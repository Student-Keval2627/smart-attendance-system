from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database.database import get_db, normalize_doc, to_object_id


student_bp = Blueprint("student_routes", __name__)
ATTENDANCE_TYPES = ("Theory", "Practical", "Tutorial")


def _get_owned_student(student_id, teacher_id):
    student_oid = to_object_id(student_id)
    teacher_oid = to_object_id(teacher_id)

    if not student_oid or not teacher_oid:
        return None, None, None

    db = get_db()
    student_doc = db.students.find_one({"_id": student_oid})
    if not student_doc:
        return None, None, None

    class_doc = db.classes.find_one({
        "_id": student_doc["class_id"],
        "teacher_id": teacher_oid
    })

    if not class_doc:
        return None, None, None

    return student_oid, student_doc, class_doc


@student_bp.route("/student/<student_id>")
def view_student(student_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    student_oid, student_doc, class_doc = _get_owned_student(
        student_id,
        session["teacher_id"]
    )

    if not student_doc:
        return "Student not found", 404

    db = get_db()
    class_oid = class_doc["_id"]

    records = list(
        db.attendance.find({
            "student_id": student_oid,
            "class_id": class_oid
        }).sort([("attendance_date", -1), ("attendance_type", 1)])
    )

    total_classes = len(records)
    present_classes = sum(1 for record in records if record.get("status") == "Present")
    attendance_percentage = round((present_classes / total_classes) * 100, 1) if total_classes else 0

    category_stats = {}
    for attendance_type in ATTENDANCE_TYPES:
        type_records = [
            record for record in records
            if record.get("attendance_type") == attendance_type
        ]
        type_total = len(type_records)
        type_present = sum(
            1 for record in type_records
            if record.get("status") == "Present"
        )
        category_stats[attendance_type] = {
            "total": type_total,
            "present": type_present,
            "percentage": round((type_present / type_total) * 100, 1) if type_total else 0
        }

    attendance_history = []
    for record in records:
        attendance_history.append({
            "attendance_date": record.get("attendance_date", ""),
            "attendance_type": record.get("attendance_type", "Theory"),
            "status": record.get("status", "Absent")
        })

    student = normalize_doc(student_doc)
    student["class_name"] = class_doc.get("class_name", "")
    student["batch"] = class_doc.get("batch", "")

    return render_template(
        "student_view.html",
        student=student,
        attendance_history=attendance_history,
        attendance_percentage=attendance_percentage,
        total_classes=total_classes,
        present_classes=present_classes,
        category_stats=category_stats
    )


@student_bp.route("/student/<student_id>/delete", methods=["GET", "POST"])
def delete_student(student_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    student_oid, student_doc, class_doc = _get_owned_student(
        student_id,
        session["teacher_id"]
    )

    if not student_doc:
        return "Student not found", 404

    db = get_db()
    class_oid = class_doc["_id"]

    student = normalize_doc(student_doc)
    student["class_name"] = class_doc.get("class_name", "")
    student["batch"] = class_doc.get("batch", "")

    if request.method == "POST":
        try:
            db.attendance.delete_many({
                "student_id": student_oid,
                "class_id": class_oid
            })
            db.students.delete_one({"_id": student_oid})
        except Exception as exc:
            print("Delete student error:", exc)
            flash("Unable to delete student. Please try again.")
            return redirect(url_for("class_routes.open_class", class_id=str(class_oid)))

        flash("Student deleted successfully.")
        return redirect(url_for("class_routes.open_class", class_id=str(class_oid)))

    return render_template("delete_student.html", student=student)
