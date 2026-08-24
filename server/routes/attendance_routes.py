from datetime import date, datetime

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


attendance_bp = Blueprint("attendance", __name__)


# ==================================================
# 1. COLLECT ATTENDANCE - SELECT DATE
# ==================================================

@attendance_bp.route(
    "/class/<int:class_id>/collect-attendance",
    methods=["GET", "POST"]
)
def collect_attendance(class_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # --------------------------------------------------
    # Check class belongs to logged-in teacher
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Teacher information
    # --------------------------------------------------

    teacher = conn.execute(
        """
        SELECT *
        FROM teachers
        WHERE id = ?
        """,
        (teacher_id,)
    ).fetchone()

    conn.close()

    # --------------------------------------------------
    # Date submit
    # --------------------------------------------------

    if request.method == "POST":

        attendance_date = request.form.get(
            "attendance_date",
            ""
        ).strip()

        # Date required
        if not attendance_date:

            flash("Please select attendance date.")

            return redirect(
                url_for(
                    "attendance.collect_attendance",
                    class_id=class_id
                )
            )

        # Validate date format
        try:

            selected_date = datetime.strptime(
                attendance_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            flash("Invalid attendance date.")

            return redirect(
                url_for(
                    "attendance.collect_attendance",
                    class_id=class_id
                )
            )

        # Future date not allowed
        if selected_date > date.today():

            flash("Future date attendance is not allowed.")

            return redirect(
                url_for(
                    "attendance.collect_attendance",
                    class_id=class_id
                )
            )

        # Store selected date temporarily
        session["attendance_date"] = attendance_date
        session["attendance_class_id"] = class_id

        return redirect(
            url_for(
                "attendance.mark_attendance",
                class_id=class_id
            )
        )

    # GET request
    return render_template(
        "collect_attendance.html",
        class_info=class_info,
        teacher=teacher,
        today=date.today().isoformat()
    )


# ==================================================
# 2. MARK / UPDATE ATTENDANCE
# ==================================================

@attendance_bp.route(
    "/class/<int:class_id>/mark-attendance",
    methods=["GET", "POST"]
)
def mark_attendance(class_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    attendance_date = session.get("attendance_date")
    attendance_class_id = session.get("attendance_class_id")

    # --------------------------------------------------
    # Check selected attendance date exists
    # --------------------------------------------------

    if not attendance_date:

        return redirect(
            url_for(
                "attendance.collect_attendance",
                class_id=class_id
            )
        )

    # --------------------------------------------------
    # Prevent date from another class being reused
    # --------------------------------------------------

    if attendance_class_id != class_id:

        session.pop("attendance_date", None)
        session.pop("attendance_class_id", None)

        return redirect(
            url_for(
                "attendance.collect_attendance",
                class_id=class_id
            )
        )

    conn = get_db_connection()

    # --------------------------------------------------
    # Check class belongs to logged-in teacher
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Teacher information
    # --------------------------------------------------

    teacher = conn.execute(
        """
        SELECT *
        FROM teachers
        WHERE id = ?
        """,
        (teacher_id,)
    ).fetchone()

    # --------------------------------------------------
    # Students + overall attendance percentage
    # + current status for selected date
    # --------------------------------------------------

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
            END AS attendance_percentage,

            (
                SELECT existing.status

                FROM attendance existing

                WHERE existing.student_id = s.id
                  AND existing.class_id = ?
                  AND existing.attendance_date = ?

                LIMIT 1
            ) AS current_status

        FROM students s

        LEFT JOIN attendance a
            ON s.id = a.student_id
           AND a.class_id = s.class_id

        WHERE s.class_id = ?

        GROUP BY s.id

        ORDER BY s.roll_no
        """,
        (
            class_id,
            attendance_date,
            class_id
        )
    ).fetchall()

    # --------------------------------------------------
    # Save / update attendance
    # --------------------------------------------------

    if request.method == "POST":

        if not students:

            conn.close()

            flash("No students found in this class.")

            return redirect(
                url_for(
                    "class_routes.open_class",
                    class_id=class_id
                )
            )

        # IDs selected as Present
        present_students = request.form.getlist(
            "present_students"
        )

        try:

            for student in students:

                student_id = student["id"]

                if str(student_id) in present_students:
                    status = "Present"
                else:
                    status = "Absent"

                conn.execute(
                    """
                    INSERT INTO attendance (
                        student_id,
                        class_id,
                        teacher_id,
                        attendance_date,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?)

                    ON CONFLICT (
                        student_id,
                        class_id,
                        attendance_date
                    )

                    DO UPDATE SET
                        status = excluded.status,
                        teacher_id = excluded.teacher_id
                    """,
                    (
                        student_id,
                        class_id,
                        teacher_id,
                        attendance_date,
                        status
                    )
                )

            conn.commit()

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Attendance save error:", e)

            flash(
                "Unable to save attendance. Please try again."
            )

            return redirect(
                url_for(
                    "attendance.mark_attendance",
                    class_id=class_id
                )
            )

        conn.close()

        # Clear temporary attendance session
        session.pop("attendance_date", None)
        session.pop("attendance_class_id", None)

        flash("Attendance submitted successfully!")

        return redirect(
            url_for(
                "class_routes.open_class",
                class_id=class_id
            )
        )

    # GET request
    conn.close()

    return render_template(
        "mark_attendance.html",
        class_info=class_info,
        teacher=teacher,
        students=students,
        attendance_date=attendance_date
    )


# ==================================================
# 3. CLASS ATTENDANCE HISTORY
# ==================================================

@attendance_bp.route(
    "/class/<int:class_id>/attendance-history"
)
def attendance_history(class_id):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # --------------------------------------------------
    # Check class belongs to logged-in teacher
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Date-wise attendance summary
    # --------------------------------------------------

    history = conn.execute(
        """
        SELECT
            attendance_date,

            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present_count,

            SUM(
                CASE
                    WHEN status = 'Absent'
                    THEN 1
                    ELSE 0
                END
            ) AS absent_count,

            COUNT(*) AS total_count

        FROM attendance

        WHERE class_id = ?
          AND teacher_id = ?

        GROUP BY attendance_date

        ORDER BY attendance_date DESC
        """,
        (class_id, teacher_id)
    ).fetchall()

    conn.close()

    return render_template(
        "attendance_history.html",
        class_info=class_info,
        history=history
    )


# ==================================================
# 4. VIEW ATTENDANCE FOR ONE DATE
# ==================================================

@attendance_bp.route(
    "/class/<int:class_id>/attendance-history/<attendance_date>"
)
def view_attendance_date(class_id, attendance_date):

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    # --------------------------------------------------
    # Validate date from URL
    # --------------------------------------------------

    try:

        datetime.strptime(
            attendance_date,
            "%Y-%m-%d"
        )

    except ValueError:

        return "Invalid attendance date", 404

    conn = get_db_connection()

    # --------------------------------------------------
    # Check class belongs to logged-in teacher
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Students + attendance status for selected date
    # --------------------------------------------------

    attendance_records = conn.execute(
        """
        SELECT
            s.name,
            s.roll_no,
            a.status

        FROM attendance a

        JOIN students s
            ON a.student_id = s.id

        WHERE a.class_id = ?
          AND a.teacher_id = ?
          AND a.attendance_date = ?

        ORDER BY s.roll_no
        """,
        (
            class_id,
            teacher_id,
            attendance_date
        )
    ).fetchall()

    conn.close()

    return render_template(
        "attendance_date_view.html",
        class_info=class_info,
        attendance_records=attendance_records,
        attendance_date=attendance_date
    )