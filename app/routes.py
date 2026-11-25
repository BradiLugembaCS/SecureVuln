
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app.models import User

from app import db
from app.models import Vulnerability

main = Blueprint("main", __name__)



@main.route("/")
@login_required
def home():
    # Show the newest vulnerability reports first.
    vulnerabilities = Vulnerability.query.order_by(
        Vulnerability.created_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        vulnerabilities=vulnerabilities
    )



@main.route("/login", methods=["GET", "POST"])
def login():
    # Logged-in users don't need to sign in again.
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Look up the account using a safe database query.
        user = User.query.filter_by(username=username).first()

        # Verify the password against its stored hash.
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.home"))

        # Use the same error for incorrect usernames and passwords.
        flash("Invalid username or password.")

    return render_template("login.html")


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    # End the session so the user must log in again.
    logout_user()
    return redirect(url_for("main.login"))



@main.route("/admin")
@login_required
def admin():
    # Only administrators should be able to access this page.
    if current_user.role != "admin":
        abort(403)

    return render_template("admin.html")



@main.route("/vulnerabilities/add", methods=["GET", "POST"])
@login_required
def add_vulnerability():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        affected_system = request.form.get("affected_system", "").strip()
        severity = request.form.get("severity", "")

        # Check the input on the server, not just in the HTML form.
        if not all([title, description, affected_system]):
            flash("All fields are required.")
        elif len(title) > 150 or len(affected_system) > 100:
            flash("Title or affected system is too long.")
        elif len(description) > 2000:
            flash("Description must be 2000 characters or fewer.")
        elif severity not in ["Low", "Medium", "High", "Critical"]:
            flash("Invalid severity selected.")
        else:
            # Store the report and link it to the logged-in user.
            vulnerability = Vulnerability(
                title=title,
                description=description,
                affected_system=affected_system,
                severity=severity,
                status="Open",
                created_by=current_user.id
            )

            db.session.add(vulnerability)
            db.session.commit()

            flash("Vulnerability added successfully.")
            return redirect(url_for("main.home"))

    return render_template("add_vulnerability.html")
