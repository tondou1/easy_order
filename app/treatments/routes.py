from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from . import bp
from .forms import TreatmentForm
from ..models import Treatment
from .. import db
from ..auth.routes import admin_required   # 既存デコレータを再利用

# 一覧 ────────────────────────────────────────
@bp.route("/treatments")
@login_required
@admin_required
def list_treatments():
    treatments = Treatment.query.order_by(Treatment.id).all()
    return render_template("treatments/list.html", treatments=treatments)

# 新規登録 ──────────────────────────────────
@bp.route("/treatments/new", methods=["GET", "POST"])
@login_required
@admin_required
def create_treatment():
    form = TreatmentForm()
    if form.validate_on_submit():
        t = Treatment(name=form.name.data,
                      price=form.price.data,
                      note=form.note.data)
        db.session.add(t)
        db.session.commit()
        flash("メニューを登録しました。")
        return redirect(url_for("treatments.list_treatments"))
    return render_template("treatments/form.html", form=form, title="メニュー登録")

# 編集 ─────────────────────────────────────
@bp.route("/treatments/<int:t_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_treatment(t_id):
    t = Treatment.query.get_or_404(t_id)
    form = TreatmentForm(obj=t)
    if form.validate_on_submit():
        form.populate_obj(t)
        db.session.commit()
        flash("更新しました。")
        return redirect(url_for("treatments.list_treatments"))
    return render_template("treatments/form.html", form=form, title="メニュー編集")

# 削除確認 & 実行 ─────────────────────────────
@bp.route("/treatments/<int:t_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_treatment(t_id):
    t = Treatment.query.get_or_404(t_id)
    if request.method == "POST":
        db.session.delete(t)
        db.session.commit()
        flash("削除しました。")
        return redirect(url_for("treatments.list_treatments"))
    return render_template("treatments/confirm_delete.html", treatment=t)
