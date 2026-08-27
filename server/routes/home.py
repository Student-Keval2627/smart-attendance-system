from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database.database import get_db, normalize_doc, normalize_docs, to_object_id, utc_now


home_bp = Blueprint("home", __name__)


@home_bp.route("/home")
def home():
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = to_object_id(session["teacher_id"])
    if not teacher_id:
        session.clear()
        return redirect(url_for("auth.login"))

    db = get_db()

    teacher = normalize_doc(db.teachers.find_one({"_id": teacher_id}))
    if not teacher:
        session.clear()
        return redirect(url_for("auth.login"))

    classes = normalize_docs(
        db.classes.find({"teacher_id": teacher_id}).sort("created_at", -1)
    )

    return render_template(
        "home.html",
        teacher=teacher,
        classes=classes
    )


@home_bp.route("/add-class", methods=["GET", "POST"])
def add_class():
    if "teacher_id" not in session:
        return redirect(url_for("auth.login"))

    teacher_id = to_object_id(session["teacher_id"])
    if not teacher_id:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        class_name = request.form.get("class_name", "").strip()
        batch = request.form.get("batch", "").strip()

        if not class_name or not batch:
            flash("Class name and batch are required.")
            return redirect(url_for("home.add_class"))

        try:
            get_db().classes.insert_one({
                "teacher_id": teacher_id,
                "class_name": class_name,
                "batch": batch,
                "created_at": utc_now()
            })
        except Exception as exc:
            print("Add class error:", exc)
            flash("Unable to add class. Please try again.")
            return redirect(url_for("home.add_class"))

        flash("Class added successfully.")
        return redirect(url_for("home.home"))

    return render_template("add_class.html")
