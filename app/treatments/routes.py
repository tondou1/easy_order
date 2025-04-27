from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import bp
from .forms import TreatmentForm
from ..models import Treatment, OrderItem
from .. import db
from ..auth.routes import admin_required   # 既存のデコレータを再利用

# ── 一覧 ───────────────────────────────────────
@bp.route("/treatments")
@login_required
@admin_required
def list_treatments():
    # active=True のものだけ一覧表示
    treatments = Treatment.query.filter_by(active=True).order_by(Treatment.id).all()
    return render_template("treatments/list.html", treatments=treatments)

# ── 新規登録 ──────────────────────────────────
@bp.route("/treatments/new", methods=["GET", "POST"])
@login_required
@admin_required
def create_treatment():
    form = TreatmentForm()
    if form.validate_on_submit():
        t = Treatment(
            name=form.name.data,
            price=form.price.data,
            note=form.note.data
        )
        db.session.add(t)
        db.session.commit()
        flash("メニューを登録しました。")
        return redirect(url_for("treatments.list_treatments"))
    return render_template("treatments/form.html", form=form, title="メニュー登録")

# ── 編集 ─────────────────────────────────────
@bp.route("/treatments/<int:t_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_treatment(t_id):
    t = Treatment.query.get_or_404(t_id)
    form = TreatmentForm(obj=t)
    if form.validate_on_submit():
        form.populate_obj(t)
        db.session.commit()
        flash("メニューを更新しました。")
        return redirect(url_for("treatments.list_treatments"))
    return render_template("treatments/form.html", form=form, title="メニュー編集")

# ── 無効化（“削除”ラベル用）トグル ───────────────────────
@bp.route("/treatments/<int:t_id>/toggle_active", methods=["POST"])
@login_required
@admin_required
def toggle_treatment(t_id):
    t = Treatment.query.get_or_404(t_id)
    # active フラグを切り替え（実体は無効化扱い）
    t.active = not t.active
    db.session.commit()
    # フラッシュメッセージを「削除」に変更
    flash("メニューを削除しました。")
    return redirect(url_for("treatments.list_treatments"))

# ── 完全削除（依存チェックあり）── optional ──────────────────────────────
@bp.route("/treatments/<int:t_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_treatment(t_id):
    t = Treatment.query.get_or_404(t_id)
    # オーダー明細に紐づいていれば削除できない
    if OrderItem.query.filter_by(treatment_id=t.id).count() > 0:
        flash("このメニューはオーダーに利用されているため、削除できません。")
        return redirect(url_for("treatments.list_treatments"))

    if request.method == "POST":
        db.session.delete(t)
        db.session.commit()
        flash("メニューを完全削除しました。")
        return redirect(url_for("treatments.list_treatments"))

    return render_template("treatments/confirm_delete.html", treatment=t)
