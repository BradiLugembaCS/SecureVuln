
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app.models import User

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def home():
    # Only logged-in users can access the dashboard.
    return render_template("dashboard.html")


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
