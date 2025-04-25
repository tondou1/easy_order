# app/routes.py

from flask import Blueprint, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # ルートURLへのアクセスは来院一覧に飛ばす
    return redirect(url_for('visits.list_visits'))
