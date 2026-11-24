
from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return "SecureVuln is running with the new structure!"
