import sqlite3

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from database.database import get_db_connection


class_bp = Blueprint("class_routes", __name__)


# ==================================================
# 1. OPEN CLASS
# ==================================================

@class_bp.route("/class/<int:class_id>")
def open_class(class_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # Check class belongs to logged-in teacher
    class_info = conn.execute(
        """
        SELECT *
        FROM classes
        WHERE id = ?
          AND teacher_id = ?
        """,
        (class_id, teacher_id)
    ).fetchone()

    if not class_info:
        conn.close()
        return "Class not found", 404

    # Get students with attendance percentage
    students = conn.execute(
        """
        SELECT
            s.*,

            CASE
                WHEN COUNT(a.id) = 0 THEN 0

                ELSE ROUND(
                    100.0 *
                    SUM(
                        CASE
                            WHEN a.status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    )
                    / COUNT(a.id),
                    1
                )
            END AS attendance_percentage

        FROM students s

        LEFT JOIN attendance a
            ON s.id = a.student_id

        WHERE s.class_id = ?

        GROUP BY s.id

        ORDER BY s.roll_no
        """,
        (class_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "class.html",
        class_info=class_info,
        students=students
    )


# ==================================================
# 2. ADD STUDENT
# ==================================================

@class_bp.route(
    "/class/<int:class_id>/add-student",
    methods=["GET", "POST"]
)
def add_student(class_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # Check class belongs to logged-in teacher
    class_info = conn.execute(
        """
        SELECT *
        FROM classes
        WHERE id = ?
          AND teacher_id = ?
        """,
        (class_id, teacher_id)
    ).fetchone()

    if not class_info:
        conn.close()
        return "Class not found", 404

    # ----------------------------------------------
    # ADD STUDENT
    # ----------------------------------------------

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        mobile = request.form.get("mobile", "").strip()

        # Validation
        if not name or not roll_no:

            conn.close()

            flash("Name and Roll Number are required.")

            return redirect(
                url_for(
                    "class_routes.add_student",
                    class_id=class_id
                )
            )

        try:

            conn.execute(
                """
                INSERT INTO students (
                    class_id,
                    name,
                    roll_no,
                    mobile
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    class_id,
                    name,
                    roll_no,
                    mobile
                )
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.rollback()
            conn.close()

            flash("Roll number already exists in this class.")

            return redirect(
                url_for(
                    "class_routes.add_student",
                    class_id=class_id
                )
            )

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Add student error:", e)

            flash("Unable to add student. Please try again.")

            return redirect(
                url_for(
                    "class_routes.add_student",
                    class_id=class_id
                )
            )

        conn.close()

        flash("Student added successfully.")

        return redirect(
            url_for(
                "class_routes.open_class",
                class_id=class_id
            )
        )

    # GET request
    conn.close()

    return render_template(
        "add_student.html",
        class_info=class_info
    )


# ==================================================
# 3. DELETE CLASS
# ==================================================

@class_bp.route(
    "/class/<int:class_id>/delete",
    methods=["GET", "POST"]
)
def delete_class(class_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # Check class belongs to logged-in teacher
    class_info = conn.execute(
        """
        SELECT *
        FROM classes
        WHERE id = ?
          AND teacher_id = ?
        """,
        (class_id, teacher_id)
    ).fetchone()

    if not class_info:
        conn.close()
        return "Class not found", 404

    # ----------------------------------------------
    # DELETE ONLY AFTER CONFIRMATION
    # ----------------------------------------------

    if request.method == "POST":

        try:

            # 1. Delete attendance records
            conn.execute(
                """
                DELETE FROM attendance
                WHERE student_id IN (
                    SELECT id
                    FROM students
                    WHERE class_id = ?
                )
                """,
                (class_id,)
            )

            # 2. Delete students
            conn.execute(
                """
                DELETE FROM students
                WHERE class_id = ?
                """,
                (class_id,)
            )

            # 3. Delete class
            conn.execute(
                """
                DELETE FROM classes
                WHERE id = ?
                  AND teacher_id = ?
                """,
                (class_id, teacher_id)
            )

            conn.commit()

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Delete class error:", e)

            flash("Unable to delete class. Please try again.")

            return redirect(
                url_for(
                    "class_routes.open_class",
                    class_id=class_id
                )
            )

        conn.close()

        flash("Class deleted successfully.")

        return redirect(
            url_for("home.home")
        )

    # GET request → confirmation page
    conn.close()

    return render_template(
        "delete_class.html",
        class_info=class_info
    )