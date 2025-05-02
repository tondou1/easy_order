from datetime import date
from flask import render_template, request
from flask_login import login_required
from . import bp
from ..models import Visit, Order   # Order をインポート

def _build_report_for_date(target):
    orders = (
        Order.query
        .join(Visit)
        .filter(Visit.visit_date == target)
        .order_by(Order.id)
        .all()
    )

    report = []
    for o in orders:
        v = o.visit
        patient = v.patient
        visit_count = len(patient.visits)  # ← ここで来院回数を取得

        items = [f"{it.treatment.name}×{it.quantity}" for it in o.items]
        report.append({
            "chart_number": v.patient.chart_number,
            "patient":      v.patient.name,
            "visit_count":  visit_count,  # ← 追加
            "treatments":   items,
            "amount":       o.total_amount,
        })
    total_amount = sum(r["amount"] for r in report)
    return report, total_amount


@bp.route("/daily")
@login_required
def daily_report():
    # 日付パラメタ ?d=YYYY-MM-DD があればそれを、なければ今日
    d = request.args.get("d")
    try:
        target = date.fromisoformat(d) if d else date.today()
    except ValueError:
        target = date.today()

    report, total_amount = _build_report_for_date(target)

    return render_template(
        "reports/daily.html",
        date=target,
        report=report,
        total_amount=total_amount,
    )

@bp.route("/daily/pdf")
@login_required
def daily_report_pdf():
    # 印刷用も同じロジック
    d = request.args.get("d")
    try:
        target = date.fromisoformat(d) if d else date.today()
    except ValueError:
        target = date.today()

    report, total_amount = _build_report_for_date(target)

    return render_template(
        "reports/daily_pdf.html",
        date=target,
        report=report,
        total_amount=total_amount,
    )
