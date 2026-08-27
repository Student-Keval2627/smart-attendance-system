from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import check_password_hash

from database.database import (
    get_db,
    normalize_doc,
    normalize_docs
)


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ==========================================
# ADMIN LOGIN
# ==========================================

@admin_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not username or not password:

            flash(
                "Username and password are required."
            )

            return redirect(
                url_for("admin.login")
            )

        db = get_db()

        admin = db.admins.find_one({
            "username": username
        })

        if (
            admin
            and check_password_hash(
                admin["password"],
                password
            )
        ):

            session.clear()

            session["admin_id"] = str(
                admin["_id"]
            )

            session["admin_username"] = (
                admin["username"]
            )

            return redirect(
                url_for("admin.dashboard")
            )

        flash("Invalid admin credentials.")

        return redirect(
            url_for("admin.login")
        )

    return render_template(
        "admin_login.html"
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin_bp.route("/dashboard")
def dashboard():

    if "admin_id" not in session:

        return redirect(
            url_for("admin.login")
        )

    db = get_db()

    teacher_count = (
        db.teachers.count_documents({})
    )

    class_count = (
        db.classes.count_documents({})
    )

    student_count = (
        db.students.count_documents({})
    )

    attendance_count = (
        db.attendance.count_documents({})
    )


    # ======================================
    # ATTENDANCE CATEGORY STATS
    # ======================================

    attendance_stats = []

    for attendance_type in [
        "Theory",
        "Practical",
        "Tutorial"
    ]:

        total = db.attendance.count_documents({
            "attendance_type": attendance_type
        })

        present = db.attendance.count_documents({
            "attendance_type": attendance_type,
            "status": "Present"
        })

        absent = db.attendance.count_documents({
            "attendance_type": attendance_type,
            "status": "Absent"
        })

        percentage = 0

        if total > 0:

            percentage = round(
                (present / total) * 100,
                1
            )

        attendance_stats.append({
            "type": attendance_type,
            "total": total,
            "present": present,
            "absent": absent,
            "percentage": percentage
        })


    # ======================================
    # RECENT TEACHERS
    # ======================================

    teachers = normalize_docs(
        db.teachers.find({})
        .sort("_id", -1)
        .limit(5)
    )


    # ======================================
    # RECENT CLASSES
    # ======================================

    classes = []

    for class_doc in (
        db.classes.find({})
        .sort("_id", -1)
        .limit(5)
    ):

        class_data = normalize_doc(
            class_doc
        )

        teacher = db.teachers.find_one({
            "_id": class_doc["teacher_id"]
        })

        class_data["teacher_name"] = (
            teacher.get("name", "")
            if teacher
            else "Unknown"
        )

        classes.append(
            class_data
        )


    # ======================================
    # RECENT STUDENTS
    # ======================================

    students = []

    for student_doc in (
        db.students.find({})
        .sort("_id", -1)
        .limit(5)
    ):

        student_data = normalize_doc(
            student_doc
        )

        class_doc = db.classes.find_one({
            "_id": student_doc["class_id"]
        })

        if class_doc:

            student_data["class_name"] = (
                class_doc.get(
                    "class_name",
                    ""
                )
            )

        else:

            student_data["class_name"] = (
                "Unknown"
            )

        students.append(
            student_data
        )


    return render_template(
        "admin_dashboard.html",
        teacher_count=teacher_count,
        class_count=class_count,
        student_count=student_count,
        attendance_count=attendance_count,
        attendance_stats=attendance_stats,
        teachers=teachers,
        classes=classes,
        students=students
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@admin_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("admin.login")
    )