import os

from flask import (
    Flask,
    redirect,
    url_for
)

from routes.auth import auth_bp
from routes.home import home_bp
from routes.class_routes import class_bp
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp


# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CLIENT_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "client"
    )
)


# ==================================================
# FLASK APPLICATION
# ==================================================

app = Flask(
    __name__,

    template_folder=os.path.join(
        CLIENT_DIR,
        "pages"
    ),

    static_folder=CLIENT_DIR,
    static_url_path="/static"
)


# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "smart-attendance-development-key"
)


# ==================================================
# REGISTER BLUEPRINTS
# ==================================================

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(class_bp)
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)


# ==================================================
# ROOT ROUTE
# ==================================================

@app.route("/")
def index():

    return redirect(
        url_for("auth.login")
    )


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
    