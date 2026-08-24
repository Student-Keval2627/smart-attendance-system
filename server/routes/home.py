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


home_bp = Blueprint("home", __name__)


# ==================================================
# 1. HOME PAGE
# ==================================================

@home_bp.route("/home")
def home():

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    conn = get_db_connection()

    # --------------------------------------------------
    # Logged-in teacher information
    # --------------------------------------------------

    teacher = conn.execute(
        """
        SELECT *
        FROM teachers
        WHERE id = ?
        """,
        (teacher_id,)
    ).fetchone()

    # Invalid / deleted teacher session
    if not teacher:

        conn.close()
        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # --------------------------------------------------
    # Logged-in teacher's classes
    # --------------------------------------------------

    classes = conn.execute(
        """
        SELECT *
        FROM classes

        WHERE teacher_id = ?

        ORDER BY id DESC
        """,
        (teacher_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "home.html",
        teacher=teacher,
        classes=classes
    )


# ==================================================
# 2. ADD NEW CLASS
# ==================================================

@home_bp.route(
    "/add-class",
    methods=["GET", "POST"]
)
def add_class():

    # Login check
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = session["teacher_id"]

    # --------------------------------------------------
    # Add class
    # --------------------------------------------------

    if request.method == "POST":

        class_name = request.form.get(
            "class_name",
            ""
        ).strip()

        batch = request.form.get(
            "batch",
            ""
        ).strip()

        # Validation
        if not class_name or not batch:

            flash("Class name and batch are required.")

            return redirect(
                url_for("home.add_class")
            )

        conn = get_db_connection()

        try:

            conn.execute(
                """
                INSERT INTO classes (
                    teacher_id,
                    class_name,
                    batch
                )
                VALUES (?, ?, ?)
                """,
                (
                    teacher_id,
                    class_name,
                    batch
                )
            )

            conn.commit()

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Add class error:", e)

            flash(
                "Unable to add class. Please try again."
            )

            return redirect(
                url_for("home.add_class")
            )

        conn.close()

        flash("Class added successfully.")

        return redirect(
            url_for("home.home")
        )

    # GET request
    return render_template(
        "add_class.html"
    )