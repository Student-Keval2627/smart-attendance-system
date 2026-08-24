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


student_bp = Blueprint("student_routes", __name__)


# ==================================================
# 1. VIEW STUDENT
# ==================================================

@student_bp.route("/student/<int:student_id>")
def view_student(student_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # --------------------------------------------------
    # Student + class information
    # --------------------------------------------------

    student = conn.execute(
        """
        SELECT
            s.*,
            c.class_name,
            c.batch

        FROM students s

        JOIN classes c
            ON s.class_id = c.id

        WHERE s.id = ?
          AND c.teacher_id = ?
        """,
        (student_id, teacher_id)
    ).fetchone()

    if not student:
        conn.close()
        return "Student not found", 404

    class_id = student["class_id"]

    # --------------------------------------------------
    # Attendance history
    # --------------------------------------------------

    attendance_history = conn.execute(
        """
        SELECT
            attendance_date,
            status

        FROM attendance

        WHERE student_id = ?
          AND class_id = ?

        ORDER BY attendance_date DESC
        """,
        (student_id, class_id)
    ).fetchall()

    # --------------------------------------------------
    # Attendance calculation
    # --------------------------------------------------

    attendance_data = conn.execute(
        """
        SELECT
            COUNT(*) AS total_classes,

            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present_classes

        FROM attendance

        WHERE student_id = ?
          AND class_id = ?
        """,
        (student_id, class_id)
    ).fetchone()

    total_classes = attendance_data["total_classes"]

    present_classes = (
        attendance_data["present_classes"] or 0
    )

    # --------------------------------------------------
    # Attendance percentage
    # --------------------------------------------------

    if total_classes > 0:

        attendance_percentage = round(
            (present_classes / total_classes) * 100,
            1
        )

    else:

        attendance_percentage = 0

    # --------------------------------------------------
    # Low attendance warning
    # --------------------------------------------------

    minimum_attendance = 75

    low_attendance = False
    classes_needed = 0

    if (
        total_classes > 0
        and attendance_percentage < minimum_attendance
    ):

        low_attendance = True

        # Number of consecutive Present classes
        # required to reach 75%
        classes_needed = max(
            0,
            (3 * total_classes) - (4 * present_classes)
        )

    # --------------------------------------------------
    # Attendance prediction
    # --------------------------------------------------

    if total_classes > 0:

        # If student attends next 5 classes
        attend_next_5 = round(
            (
                (present_classes + 5)
                /
                (total_classes + 5)
            ) * 100,
            1
        )

        # If student misses next 3 classes
        miss_next_3 = round(
            (
                present_classes
                /
                (total_classes + 3)
            ) * 100,
            1
        )

    else:

        attend_next_5 = 100
        miss_next_3 = 0

    conn.close()

    # --------------------------------------------------
    # Send data to template
    # --------------------------------------------------

    return render_template(
        "student_view.html",
        student=student,
        attendance_history=attendance_history,
        attendance_percentage=attendance_percentage,
        total_classes=total_classes,
        present_classes=present_classes,
        low_attendance=low_attendance,
        classes_needed=classes_needed,
        attend_next_5=attend_next_5,
        miss_next_3=miss_next_3
    )


# ==================================================
# 2. DELETE STUDENT
# ==================================================

@student_bp.route(
    "/student/<int:student_id>/delete",
    methods=["GET", "POST"]
)
def delete_student(student_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # --------------------------------------------------
    # Check student belongs to logged-in teacher
    # --------------------------------------------------

    student = conn.execute(
        """
        SELECT
            s.*,
            c.class_name,
            c.batch

        FROM students s

        JOIN classes c
            ON s.class_id = c.id

        WHERE s.id = ?
          AND c.teacher_id = ?
        """,
        (student_id, teacher_id)
    ).fetchone()

    if not student:
        conn.close()
        return "Student not found", 404

    class_id = student["class_id"]

    # --------------------------------------------------
    # Delete only after confirmation
    # --------------------------------------------------

    if request.method == "POST":

        try:

            # 1. Delete attendance records
            conn.execute(
                """
                DELETE FROM attendance

                WHERE student_id = ?
                  AND class_id = ?
                """,
                (student_id, class_id)
            )

            # 2. Delete student
            conn.execute(
                """
                DELETE FROM students

                WHERE id = ?
                  AND class_id = ?
                """,
                (student_id, class_id)
            )

            conn.commit()

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Delete student error:", e)

            flash(
                "Unable to delete student. Please try again."
            )

            return redirect(
                url_for(
                    "class_routes.open_class",
                    class_id=class_id
                )
            )

        conn.close()

        flash("Student deleted successfully.")

        return redirect(
            url_for(
                "class_routes.open_class",
                class_id=class_id
            )
        )

    # --------------------------------------------------
    # GET request → confirmation page
    # --------------------------------------------------

    conn.close()

    return render_template(
        "delete_student.html",
        student=student
    )