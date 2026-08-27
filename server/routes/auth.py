from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash, generate_password_hash

from database.database import get_db, normalize_doc, to_object_id, utc_now


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("auth.register"))

        db = get_db()

        try:
            result = db.teachers.insert_one({
                "username": username,
                "password": generate_password_hash(password),
                "name": "",
                "mobile": "",
                "age": None,
                "qualification": "",
                "created_at": utc_now()
            })
        except DuplicateKeyError:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))
        except Exception as exc:
            print("Register error:", exc)
            flash("Unable to create account. Please try again.")
            return redirect(url_for("auth.register"))

        session.clear()
        session["teacher_id"] = str(result.inserted_id)
        session["username"] = username
        return redirect(url_for("auth.profile"))

    return render_template("create_account.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please enter username and password.")
            return redirect(url_for("auth.login"))

        teacher_doc = get_db().teachers.find_one({"username": username})

        if teacher_doc and check_password_hash(teacher_doc["password"], password):
            teacher = normalize_doc(teacher_doc)
            session.clear()
            session["teacher_id"] = teacher["id"]
            session["username"] = teacher["username"]

            if not teacher.get("name"):
                return redirect(url_for("auth.profile"))

            return redirect(url_for("home.home"))

        flash("Invalid username or password.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = to_object_id(session["teacher_id"])
    if not teacher_id:
        session.clear()
        return redirect(url_for("auth.login"))

    db = get_db()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        age = request.form.get("age", "").strip()
        qualification = request.form.get("qualification", "").strip()

        if not name:
            flash("Teacher name is required.")
            return redirect(url_for("auth.profile"))

        age_value = None
        if age:
            try:
                age_value = int(age)
            except ValueError:
                flash("Age must be a valid number.")
                return redirect(url_for("auth.profile"))

            if age_value <= 0:
                flash("Age must be greater than 0.")
                return redirect(url_for("auth.profile"))

        db.teachers.update_one(
            {"_id": teacher_id},
            {"$set": {
                "name": name,
                "mobile": mobile,
                "age": age_value,
                "qualification": qualification
            }}
        )

        flash("Profile updated successfully.")
        return redirect(url_for("home.home"))

    teacher = normalize_doc(db.teachers.find_one({"_id": teacher_id}))

    if not teacher:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template("profile.html", teacher=teacher)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
