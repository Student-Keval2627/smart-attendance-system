from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from pymongo.errors import DuplicateKeyError

from database.database import get_db, normalize_doc, normalize_docs, to_object_id, utc_now


class_bp = Blueprint("class_routes", __name__)


def _owned_class(class_id, teacher_id):
    class_oid = to_object_id(class_id)
    teacher_oid = to_object_id(teacher_id)

    if not class_oid or not teacher_oid:
        return None, None

    class_doc = get_db().classes.find_one({
        "_id": class_oid,
        "teacher_id": teacher_oid
    })

    return class_oid, class_doc


@class_bp.route("/class/<class_id>")
def open_class(class_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    class_oid, class_doc = _owned_class(class_id, session["teacher_id"])
    if not class_doc:
        return "Class not found", 404

    db = get_db()
    class_info = normalize_doc(class_doc)
    student_docs = list(db.students.find({"class_id": class_oid}).sort("roll_no", 1))

    students = []
    for student_doc in student_docs:
        student_oid = student_doc["_id"]
        total = db.attendance.count_documents({
            "student_id": student_oid,
            "class_id": class_oid
        })
        present = db.attendance.count_documents({
            "student_id": student_oid,
            "class_id": class_oid,
            "status": "Present"
        })

        student = normalize_doc(student_doc)
        student["attendance_percentage"] = round((present / total) * 100, 1) if total else 0
        students.append(student)

    return render_template(
        "class.html",
        class_info=class_info,
        students=students
    )


@class_bp.route("/class/<class_id>/add-student", methods=["GET", "POST"])
def add_student(class_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    class_oid, class_doc = _owned_class(class_id, session["teacher_id"])
    if not class_doc:
        return "Class not found", 404

    class_info = normalize_doc(class_doc)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        mobile = request.form.get("mobile", "").strip()

        if not name or not roll_no:
            flash("Name and Roll Number are required.")
            return redirect(url_for("class_routes.add_student", class_id=class_id))

        try:
            get_db().students.insert_one({
                "class_id": class_oid,
                "name": name,
                "roll_no": roll_no,
                "mobile": mobile,
                "created_at": utc_now()
            })
        except DuplicateKeyError:
            flash("Roll number already exists in this class.")
            return redirect(url_for("class_routes.add_student", class_id=class_id))
        except Exception as exc:
            print("Add student error:", exc)
            flash("Unable to add student. Please try again.")
            return redirect(url_for("class_routes.add_student", class_id=class_id))

        flash("Student added successfully.")
        return redirect(url_for("class_routes.open_class", class_id=class_id))

    return render_template("add_student.html", class_info=class_info)


@class_bp.route("/class/<class_id>/delete", methods=["GET", "POST"])
def delete_class(class_id):
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    class_oid, class_doc = _owned_class(class_id, session["teacher_id"])
    if not class_doc:
        return "Class not found", 404

    class_info = normalize_doc(class_doc)

    if request.method == "POST":
        db = get_db()

        try:
            db.attendance.delete_many({"class_id": class_oid})
            db.students.delete_many({"class_id": class_oid})
            db.classes.delete_one({"_id": class_oid})
        except Exception as exc:
            print("Delete class error:", exc)
            flash("Unable to delete class. Please try again.")
            return redirect(url_for("class_routes.open_class", class_id=class_id))

        flash("Class deleted successfully.")
        return redirect(url_for("home.home"))

    return render_template("delete_class.html", class_info=class_info)
