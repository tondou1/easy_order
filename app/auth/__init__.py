from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='../templates/auth')

from . import routes   # noqa: E402  (ルート登録)
