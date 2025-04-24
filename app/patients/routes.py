from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import bp
from .forms import PatientForm
from ..models import Patient        # ← DB モデル
from .. import db

# 一覧 ─────────────────────────────────────────────────────
@bp.route("/patients")
@login_required
def list_patients():
    patients = Patient.query.order_by(Patient.chart_number).all()
    return render_template("patients/list.html", patients=patients)

# 新規登録 ───────────────────────────────────────────────
@bp.route("/patients/new", methods=["GET", "POST"])
@login_required
def create_patient():
    form = PatientForm()
    if form.validate_on_submit():
        if Patient.query.filter_by(chart_number=form.chart_number.data).first():
            flash("そのカルテ番号は既に登録されています。")
        else:
            patient = Patient(
                chart_number=form.chart_number.data,
                name=form.name.data,
                furigana=form.furigana.data,
                birth_date=form.birth_date.data,
                gender=form.gender.data,
                emergency_contact=form.emergency_contact.data,
            )
            db.session.add(patient)
            db.session.commit()
            flash("患者を登録しました。")
            return redirect(url_for("patients.list_patients"))
    return render_template("patients/form.html", form=form, title="患者登録")

# 編集 ──────────────────────────────────────────────
@bp.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        # chart_number が被らないかチェック
        dup = Patient.query.filter_by(chart_number=form.chart_number.data).first()
        if dup and dup.id != patient.id:
            flash("そのカルテ番号は既に他の患者に使われています。")
        else:
            form.populate_obj(patient)
            db.session.commit()
            flash("更新しました。")
            return redirect(url_for("patients.list_patients"))
    return render_template("patients/form.html", form=form, title="患者編集")

# 削除確認 & 実行 ────────────────────────────────────────
@bp.route("/patients/<int:patient_id>/delete", methods=["GET", "POST"])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        db.session.delete(patient)
        db.session.commit()
        flash("削除しました。")
        return redirect(url_for("patients.list_patients"))
    return render_template("patients/confirm_delete.html", patient=patient)
