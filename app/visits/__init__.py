from flask import Blueprint
bp = Blueprint("visits", __name__, template_folder="../templates/visits")
from . import routes  # noqa: E402
