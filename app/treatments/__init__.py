from flask import Blueprint
bp = Blueprint("treatments", __name__, template_folder="../templates/treatments")
from . import routes  # noqa: E402
