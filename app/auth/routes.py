# app/auth/routes.py

from functools import wraps
from urllib.parse import urlparse      # ← Werkzeug ではなく標準ライブラリを使用
from flask import (
    render_template, redirect, url_for, flash, request
)
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from . import bp                       # Blueprint
from .forms import LoginForm, RegisterForm, EditUserForm
from ..models import User
from .. import db

# ──────────────────────────────────────────────────────────────
# 管理者だけに許可するデコレータ
# ──────────────────────────────────────────────────────────────
def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("管理者権限が必要です。")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapped

# ──────────────────────────────────────────────────────────────
# ログイン
# ──────────────────────────────────────────────────────────────
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_id=form.login_id.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

            nxt = request.args.get("next")
            # 外部サイトへの open redirect を防ぐ
            if not nxt or urlparse(nxt).netloc != "":
                nxt = url_for('visits.list_visits')
            return redirect(nxt)

        flash("ユーザー名またはパスワードが間違っています。")

    return render_template("auth/login.html", form=form)

# ──────────────────────────────────────────────────────────────
# ログアウト
# ──────────────────────────────────────────────────────────────
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。")
    return redirect(url_for("auth.login"))

# ──────────────────────────────────────────────────────────────
# ユーザー登録（管理者のみ）
# ──────────────────────────────────────────────────────────────
@bp.route("/register", methods=["GET", "POST"])
@admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 同名ユーザーの重複チェック
        if User.query.filter_by(login_id=form.login_id.data).first():
            flash("そのログインIDは既に存在します。")
        else:
            user = User(
                login_id=form.login_id.data,
                name=form.name.data,
                role=form.role.data                # "admin" / "staff"
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            flash("ユーザーを作成しました。")
            return redirect(url_for("auth.register"))

    # 既存ユーザー一覧も取得
    users = User.query.order_by(User.id).all()
    return render_template("auth/register.html", form=form, users=users)

# ──────────────────────────────────────────────────────────────
# ユーザー編集
# ──────────────────────────────────────────────────────────────
@bp.route("/register/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.login_id = form.login_id.data
        user.name     = form.name.data
        user.role     = form.role.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("ユーザー情報を更新しました。")
        return redirect(url_for("auth.register"))
    return render_template("auth/edit_user.html", form=form, user=user)

# ──────────────────────────────────────────────────────────────
# ユーザー削除
# ──────────────────────────────────────────────────────────────
@bp.route("/register/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("自分自身は削除できません。")
    else:
        db.session.delete(user)
        db.session.commit()
        flash("ユーザーを削除しました。")
    return redirect(url_for("auth.register"))
