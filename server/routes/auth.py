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

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.database import get_db_connection


auth_bp = Blueprint("auth", __name__)


# ==================================================
# 1. CREATE TEACHER ACCOUNT
# ==================================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if not username or not password:

            flash("Username and password are required.")

            return redirect(
                url_for("auth.register")
            )

        # Hash password before saving
        hashed_password = generate_password_hash(
            password
        )

        conn = get_db_connection()

        try:

            cursor = conn.execute(
                """
                INSERT INTO teachers (
                    username,
                    password
                )
                VALUES (?, ?)
                """,
                (
                    username,
                    hashed_password
                )
            )

            conn.commit()

            teacher_id = cursor.lastrowid

        except sqlite3.IntegrityError:

            conn.rollback()
            conn.close()

            flash("Username already exists.")

            return redirect(
                url_for("auth.register")
            )

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Register error:", e)

            flash(
                "Unable to create account. Please try again."
            )

            return redirect(
                url_for("auth.register")
            )

        conn.close()

        # Start a clean login session
        session.clear()

        session["teacher_id"] = teacher_id
        session["username"] = username

        # New teacher completes profile first
        return redirect(
            url_for("auth.profile")
        )

    return render_template(
        "create_account.html"
    )


# ==================================================
# 2. TEACHER LOGIN
# ==================================================

@auth_bp.route(
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

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if not username or not password:

            flash("Please enter username and password.")

            return redirect(
                url_for("auth.login")
            )

        conn = get_db_connection()

        teacher = conn.execute(
            """
            SELECT *
            FROM teachers
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        conn.close()

        # --------------------------------------------------
        # Username + password check
        # --------------------------------------------------

        if (
            teacher
            and check_password_hash(
                teacher["password"],
                password
            )
        ):

            # Remove any previous session data
            session.clear()

            session["teacher_id"] = teacher["id"]
            session["username"] = teacher["username"]

            # Profile not completed yet
            if not teacher["name"]:

                return redirect(
                    url_for("auth.profile")
                )

            # Profile complete
            return redirect(
                url_for("home.home")
            )

        flash("Invalid username or password.")

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "login.html"
    )


# ==================================================
# 3. TEACHER PROFILE
# ==================================================

@auth_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
def profile():

    # Login check
    if "teacher_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    teacher_id = session["teacher_id"]

    # --------------------------------------------------
    # UPDATE PROFILE
    # --------------------------------------------------

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        qualification = request.form.get(
            "qualification",
            ""
        ).strip()

        # Name required
        if not name:

            flash("Teacher name is required.")

            return redirect(
                url_for("auth.profile")
            )

        # Validate age if entered
        age_value = None

        if age:

            try:
                age_value = int(age)

            except ValueError:

                flash("Age must be a valid number.")

                return redirect(
                    url_for("auth.profile")
                )

            if age_value <= 0:

                flash("Age must be greater than 0.")

                return redirect(
                    url_for("auth.profile")
                )

        conn = get_db_connection()

        try:

            conn.execute(
                """
                UPDATE teachers

                SET
                    name = ?,
                    mobile = ?,
                    age = ?,
                    qualification = ?

                WHERE id = ?
                """,
                (
                    name,
                    mobile,
                    age_value,
                    qualification,
                    teacher_id
                )
            )

            conn.commit()

        except Exception as e:

            conn.rollback()
            conn.close()

            print("Profile update error:", e)

            flash(
                "Unable to update profile. Please try again."
            )

            return redirect(
                url_for("auth.profile")
            )

        conn.close()

        flash("Profile updated successfully.")

        return redirect(
            url_for("home.home")
        )

    # --------------------------------------------------
    # GET PROFILE
    # --------------------------------------------------

    conn = get_db_connection()

    teacher = conn.execute(
        """
        SELECT *
        FROM teachers
        WHERE id = ?
        """,
        (teacher_id,)
    ).fetchone()

    conn.close()

    # Invalid or deleted teacher session
    if not teacher:

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "profile.html",
        teacher=teacher
    )


# ==================================================
# 4. LOGOUT
# ==================================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )