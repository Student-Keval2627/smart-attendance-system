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


# ==================================================
# ADMIN LOGIN
# ==================================================

@admin_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # Already logged in
    if "admin_id" in session:
        return redirect(
            url_for("admin.dashboard")
        )

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
                admin.get("password", ""),
                password
            )
        ):

            session.clear()

            session["admin_id"] = str(
                admin["_id"]
            )

            session["admin_username"] = (
                admin.get(
                    "username",
                    "admin"
                )
            )

            return redirect(
                url_for("admin.dashboard")
            )

        flash(
            "Invalid admin credentials."
        )

        return redirect(
            url_for("admin.login")
        )

    return render_template(
        "admin_login.html"
    )


# ==================================================
# ADMIN DASHBOARD
# ==================================================

@admin_bp.route("/dashboard")
def dashboard():

    if "admin_id" not in session:

        return redirect(
            url_for("admin.login")
        )

    db = get_db()


    # ==================================================
    # MAIN COUNTS
    # ==================================================

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


    # ==================================================
    # ATTENDANCE CATEGORY STATS
    # ==================================================

    attendance_stats = []

    for attendance_type in [
        "Theory",
        "Practical",
        "Tutorial"
    ]:

        total = (
            db.attendance.count_documents({
                "attendance_type": attendance_type
            })
        )

        present = (
            db.attendance.count_documents({
                "attendance_type": attendance_type,
                "status": "Present"
            })
        )

        absent = (
            db.attendance.count_documents({
                "attendance_type": attendance_type,
                "status": "Absent"
            })
        )

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


    # ==================================================
    # RECENT TEACHERS
    # ==================================================

    teacher_cursor = (
        db.teachers
        .find({})
        .sort("_id", -1)
        .limit(5)
    )

    teachers = normalize_docs(
        teacher_cursor
    )


    # ==================================================
    # RECENT CLASSES
    # ==================================================

    classes = []

    class_cursor = (
        db.classes
        .find({})
        .sort("_id", -1)
        .limit(5)
    )

    for class_doc in class_cursor:

        class_data = normalize_doc(
            class_doc
        )

        teacher_name = (
            "Unknown Teacher"
        )

        teacher_id = class_doc.get(
            "teacher_id"
        )

        if teacher_id:

            teacher_doc = (
                db.teachers.find_one({
                    "_id": teacher_id
                })
            )

            if teacher_doc:

                teacher_name = (
                    teacher_doc.get("name")
                    or teacher_doc.get(
                        "username",
                        "Unknown Teacher"
                    )
                )

        class_data[
            "teacher_name"
        ] = teacher_name

        classes.append(
            class_data
        )


    # ==================================================
    # RECENT STUDENTS
    # ==================================================

    students = []

    student_cursor = (
        db.students
        .find({})
        .sort("_id", -1)
        .limit(5)
    )

    for student_doc in student_cursor:

        student_data = normalize_doc(
            student_doc
        )

        class_name = (
            "Unknown Class"
        )

        class_id = student_doc.get(
            "class_id"
        )

        if class_id:

            class_doc = (
                db.classes.find_one({
                    "_id": class_id
                })
            )

            if class_doc:

                class_name = (
                    class_doc.get(
                        "class_name"
                    )
                    or class_doc.get(
                        "name"
                    )
                    or "Unknown Class"
                )

        student_data[
            "class_name"
        ] = class_name

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


# ==================================================
# TEACHERS MANAGEMENT
# ==================================================

@admin_bp.route("/teachers")
def teachers():

    if "admin_id" not in session:

        return redirect(
            url_for("admin.login")
        )

    db = get_db()

    search = request.args.get(
        "search",
        ""
    ).strip()


    # ==================================================
    # SEARCH QUERY
    # ==================================================

    query = {}

    if search:

        query = {
            "$or": [

                {
                    "name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "username": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "mobile": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]
        }


    # ==================================================
    # FETCH TEACHERS
    # ==================================================

    teacher_docs = list(
        db.teachers
        .find(query)
        .sort("_id", -1)
    )

    teacher_list = []


    # ==================================================
    # TEACHER STATISTICS
    # ==================================================

    for teacher_doc in teacher_docs:

        teacher_data = normalize_doc(
            teacher_doc
        )

        teacher_id = teacher_doc[
            "_id"
        ]


        # ----------------------------------------------
        # CLASS COUNT
        # ----------------------------------------------

        class_count = (
            db.classes.count_documents({
                "teacher_id": teacher_id
            })
        )


        # ----------------------------------------------
        # GET CLASS IDS
        # ----------------------------------------------

        class_ids = []

        class_cursor = (
            db.classes.find(
                {
                    "teacher_id": teacher_id
                },
                {
                    "_id": 1
                }
            )
        )

        for class_doc in class_cursor:

            class_ids.append(
                class_doc["_id"]
            )


        # ----------------------------------------------
        # STUDENT COUNT
        # ----------------------------------------------

        student_count = 0

        if class_ids:

            student_count = (
                db.students.count_documents({
                    "class_id": {
                        "$in": class_ids
                    }
                })
            )


        teacher_data[
            "class_count"
        ] = class_count

        teacher_data[
            "student_count"
        ] = student_count

        teacher_list.append(
            teacher_data
        )


    return render_template(
        "admin_teachers.html",

        teachers=teacher_list,
        search=search
    )

# ==================================================
# CLASSES MANAGEMENT
# ==================================================

@admin_bp.route("/classes")
def classes():

    if "admin_id" not in session:
        return redirect(
            url_for("admin.login")
        )

    db = get_db()

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = {}

    if search:

        teacher_ids = []

        teacher_cursor = db.teachers.find({
            "$or": [
                {
                    "name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "username": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]
        })

        teacher_ids = [
            teacher["_id"]
            for teacher in teacher_cursor
        ]

        query = {
            "$or": [
                {
                    "class_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "batch": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]
        }

        if teacher_ids:
            query["$or"].append({
                "teacher_id": {
                    "$in": teacher_ids
                }
            })

    class_docs = list(
        db.classes
        .find(query)
        .sort("_id", -1)
    )

    class_list = []

    for class_doc in class_docs:

        class_data = normalize_doc(
            class_doc
        )

        teacher_name = "Unknown Teacher"

        teacher_id = class_doc.get(
            "teacher_id"
        )

        if teacher_id:

            teacher_doc = (
                db.teachers.find_one({
                    "_id": teacher_id
                })
            )

            if teacher_doc:

                teacher_name = (
                    teacher_doc.get("name")
                    or teacher_doc.get(
                        "username",
                        "Unknown Teacher"
                    )
                )

        student_count = (
            db.students.count_documents({
                "class_id": class_doc["_id"]
            })
        )

        class_data[
            "teacher_name"
        ] = teacher_name

        class_data[
            "student_count"
        ] = student_count

        class_list.append(
            class_data
        )

    return render_template(
        "admin_classes.html",
        classes=class_list,
        search=search
    )
# ==================================================
# STUDENTS MANAGEMENT
# ==================================================

@admin_bp.route("/students")
def students():

    if "admin_id" not in session:
        return redirect(
            url_for("admin.login")
        )

    db = get_db()

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = {}

    if search:

        # Find teachers matching search
        teacher_ids = [
            teacher["_id"]
            for teacher in db.teachers.find({
                "$or": [
                    {
                        "name": {
                            "$regex": search,
                            "$options": "i"
                        }
                    },
                    {
                        "username": {
                            "$regex": search,
                            "$options": "i"
                        }
                    }
                ]
            })
        ]

        # Find classes matching class/batch/teacher
        class_query = {
            "$or": [
                {
                    "class_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "batch": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]
        }

        if teacher_ids:
            class_query["$or"].append({
                "teacher_id": {
                    "$in": teacher_ids
                }
            })

        matching_class_ids = [
            class_doc["_id"]
            for class_doc in db.classes.find(
                class_query,
                {"_id": 1}
            )
        ]

        query = {
            "$or": [
                {
                    "name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "roll_no": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "mobile": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]
        }

        if matching_class_ids:
            query["$or"].append({
                "class_id": {
                    "$in": matching_class_ids
                }
            })

    student_docs = list(
        db.students
        .find(query)
        .sort("_id", -1)
    )

    student_list = []

    for student_doc in student_docs:

        student_data = normalize_doc(
            student_doc
        )

        class_name = "Unknown Class"
        batch = "-"
        teacher_name = "Unknown Teacher"

        class_doc = db.classes.find_one({
            "_id": student_doc.get("class_id")
        })

        if class_doc:

            class_name = (
                class_doc.get("class_name")
                or "Unknown Class"
            )

            batch = (
                class_doc.get("batch")
                or "-"
            )

            teacher_id = class_doc.get(
                "teacher_id"
            )

            if teacher_id:

                teacher_doc = (
                    db.teachers.find_one({
                        "_id": teacher_id
                    })
                )

                if teacher_doc:

                    teacher_name = (
                        teacher_doc.get("name")
                        or teacher_doc.get(
                            "username",
                            "Unknown Teacher"
                        )
                    )

        total = db.attendance.count_documents({
            "student_id": student_doc["_id"]
        })

        present = db.attendance.count_documents({
            "student_id": student_doc["_id"],
            "status": "Present"
        })

        attendance_percentage = 0

        if total > 0:
            attendance_percentage = round(
                (present / total) * 100,
                1
            )

        student_data["class_name"] = class_name
        student_data["batch"] = batch
        student_data["teacher_name"] = teacher_name
        student_data["attendance_percentage"] = (
            attendance_percentage
        )

        student_list.append(
            student_data
        )

    return render_template(
        "admin_students.html",
        students=student_list,
        search=search
    )
# ==================================================
# ADMIN LOGOUT
# ==================================================

@admin_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("admin.login")
    )