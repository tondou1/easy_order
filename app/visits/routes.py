from datetime import date
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import bp
from .forms import VisitForm
from ..models import Visit, Patient
from .. import db

# 一覧 ─────────────────────────────────────
@bp.route("/visits")
@login_required
def list_visits():
    # ?d=YYYY-MM-DD を指定しなければ今日
    target_date = request.args.get("d", date.today().isoformat())
    visits = (Visit.query
              .filter_by(visit_date=target_date)
              .order_by(Visit.id)
              .all())
    return render_template("visits/list.html",
                           visits=visits,
                           target_date=target_date)

# 新規登録 ───────────────────────────────
@bp.route("/visits/new", methods=["GET", "POST"])
@login_required
def create_visit():
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit(
            patient_id=form.patient_id.data,
            user_id=current_user.id,
            visit_date=form.visit_date.data
        )
        db.session.add(visit)
        db.session.commit()
        flash("来院を登録しました。")
        return redirect(url_for("visits.list_visits"))
    return render_template("visits/form.html", form=form, title="来院登録")

# 編集 ──────────────────────────────────
@bp.route("/visits/<int:visit_id>/edit", methods=["GET", "POST"])
@login_required
def edit_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    form = VisitForm(obj=visit)
    if form.validate_on_submit():
        visit.patient_id = form.patient_id.data
        visit.visit_date = form.visit_date.data
        db.session.commit()
        flash("更新しました。")
        return redirect(url_for("visits.list_visits", d=visit.visit_date))
    return render_template("visits/form.html", form=form, title="来院編集")

# 削除確認・実行 ──────────────────────────
@bp.route("/visits/<int:visit_id>/delete", methods=["GET", "POST"])
@login_required
def delete_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    if request.method == "POST":
        target_date = visit.visit_date
        db.session.delete(visit)
        db.session.commit()
        flash("削除しました。")
        return redirect(url_for("visits.list_visits", d=target_date))
    return render_template("visits/confirm_delete.html", visit=visit)
