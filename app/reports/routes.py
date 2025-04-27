# app/reports/routes.py

from datetime import date
from flask import render_template, request
from flask_login import login_required
from . import bp
from ..models import Visit

@bp.route("/daily")
@login_required
def daily_report():
    # 日付パラメタ ?d=YYYY-MM-DD があればそれを、なければ今日
    d = request.args.get("d")
    try:
        target = date.fromisoformat(d) if d else date.today()
    except ValueError:
        target = date.today()

    visits = (
        Visit.query
        .filter_by(visit_date=target)
        .order_by(Visit.id)
        .all()
    )

    report = []
    for v in visits:
        order = v.orders[-1] if v.orders else None
        # メニュー名×数量 のリスト
        items = [f"{it.treatment.name}×{it.quantity}" for it in (order.items if order else [])]
        report.append({
            "visit_id":   v.id,
            "patient":    v.patient.name,
            "staff":      v.staff.name,
            "treatments": items,
            "amount":     order.total_amount if order else 0,
        })

    total_amount = sum(r["amount"] for r in report)

    return render_template(
        "reports/daily.html",
        date=target,
        report=report,
        total_amount=total_amount,
    )

@bp.route("/daily/pdf")
@login_required
def daily_report_pdf():
    # daily_report() と同じロジックをコピー
    d = request.args.get("d")
    try:
        target = date.fromisoformat(d) if d else date.today()
    except ValueError:
        target = date.today()

    visits = (
        Visit.query
        .filter_by(visit_date=target)
        .order_by(Visit.id)
        .all()
    )

    report = []
    for v in visits:
        order = v.orders[-1] if v.orders else None
        items = [f"{it.treatment.name}×{it.quantity}" for it in (order.items if order else [])]
        report.append({
            "visit_id":   v.id,
            "patient":    v.patient.name,
            "staff":      v.staff.name,
            "treatments": items,
            "amount":     order.total_amount if order else 0,
        })

    total_amount = sum(r["amount"] for r in report)

    # 印刷用テンプレートを返す
    return render_template(
        "reports/daily_pdf.html",
        date=target,
        report=report,
        total_amount=total_amount,
    )
