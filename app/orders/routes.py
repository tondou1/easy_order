# app/orders/routes.py
from flask import (
    render_template, redirect, url_for, flash, request
)
from flask_login import login_required, current_user
from . import bp
from .forms import OrderItemForm
from ..models import Visit, Order, OrderItem, Treatment
from .. import db


# ────────────────────────────────────────────────────────────
# 内部ヘルパー
# ────────────────────────────────────────────────────────────
def get_or_create_order(visit_id: int) -> Order:
    """Visit にひも付く Order を 1 件だけ保証して返す"""
    visit = Visit.query.get_or_404(visit_id)
    if not visit.orders:
        order = Order(
            visit_id=visit.id,
            user_id=current_user.id,
            created_at=visit.visit_date,
        )
        db.session.add(order)
        db.session.commit()
    else:
        order = visit.orders[0]
    return order


# ────────────────────────────────────────────────────────────
# オーダー詳細 + 明細追加
# ────────────────────────────────────────────────────────────
@bp.route("/visits/<int:visit_id>/order", methods=["GET", "POST"])
@login_required
def order_view(visit_id):
    order = get_or_create_order(visit_id)
    form = OrderItemForm()

    if form.validate_on_submit():
        treatment = Treatment.query.get_or_404(form.treatment_id.data)

        # ★ subtotal をここで直接計算してセット ★
        item = OrderItem(
            order_id=order.id,
            treatment_id=treatment.id,
            quantity=form.quantity.data,
            subtotal=treatment.price * form.quantity.data,
        )
        db.session.add(item)
        db.session.commit()

        # 合計を再計算して保存
        order.recalc_total()
        db.session.commit()

        flash("明細を追加しました。")
        return redirect(url_for("orders.order_view", visit_id=visit_id))

    return render_template("orders/order.html", order=order, form=form)


# ────────────────────────────────────────────────────────────
# 明細編集
# ────────────────────────────────────────────────────────────
@bp.route("/orders/item/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    form = OrderItemForm(obj=item)

    if form.validate_on_submit():
        treatment = Treatment.query.get_or_404(form.treatment_id.data)

        item.treatment_id = treatment.id
        item.quantity = form.quantity.data
        item.subtotal = treatment.price * form.quantity.data  # 再計算

        item.order.recalc_total()
        db.session.commit()

        flash("更新しました。")
        return redirect(url_for("orders.order_view", visit_id=item.order.visit_id))

    return render_template("orders/item_form.html", form=form, title="明細編集")


# ────────────────────────────────────────────────────────────
# 明細削除
# ────────────────────────────────────────────────────────────
@bp.route("/orders/item/<int:item_id>/delete", methods=["GET", "POST"])
@login_required
def delete_item(item_id):
    item = OrderItem.query.get_or_404(item_id)

    if request.method == "POST":
        visit_id = item.order.visit_id
        db.session.delete(item)
        db.session.commit()

        # 合計を再計算
        item.order.recalc_total()
        db.session.commit()

        flash("削除しました。")
        return redirect(url_for("orders.order_view", visit_id=visit_id))

    return render_template("orders/confirm_delete.html", item=item)


# ────────────────────────────────────────────────────────────
# 支払ステータス切替
# ────────────────────────────────────────────────────────────
@bp.route("/orders/<int:order_id>/toggle")
@login_required
def toggle_payment(order_id):
    order = Order.query.get_or_404(order_id)
    order.payment_status = "paid" if order.payment_status == "unpaid" else "unpaid"
    db.session.commit()

    flash("支払ステータスを更新しました。")
    return redirect(url_for("orders.order_view", visit_id=order.visit_id))
