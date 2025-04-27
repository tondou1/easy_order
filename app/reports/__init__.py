# app/reports/__init__.py

from flask import Blueprint

# Blueprint の名前は “reports” 、URL プレフィックスは /reports
bp = Blueprint('reports', __name__, url_prefix='/reports')

# ルートハンドラを読み込む
from . import routes
