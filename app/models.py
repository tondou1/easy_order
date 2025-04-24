# app/models.py
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager   # __init__.py で用意済み

# ---------- 1) ユーザ ----------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role          = db.Column(db.String(10), nullable=False, default="staff")  # "admin" / "staff"

    # 関連
    visits = db.relationship("Visit",  back_populates="staff",   cascade="all, delete-orphan")
    orders = db.relationship("Order",  back_populates="cashier", cascade="all, delete-orphan")

    # ― Flask-Login 用
    def get_id(self):
        return str(self.id)

    # ― パスワード操作
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- 2) 患者 ----------
class Patient(db.Model):
    __tablename__ = "patients"

    id               = db.Column(db.Integer, primary_key=True)
    chart_number     = db.Column(db.String(20),  unique=True, nullable=False)
    name             = db.Column(db.String(64),  nullable=False)
    furigana         = db.Column(db.String(64))
    birth_date       = db.Column(db.Date)
    gender           = db.Column(db.String(10))
    emergency_contact= db.Column(db.String(64))

    visits = db.relationship("Visit", back_populates="patient", cascade="all, delete-orphan")

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None


# ---------- 3) 来院 ----------
class Visit(db.Model):
    __tablename__ = "visits"

    id         = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"),    nullable=False)  # 受付担当
    visit_date = db.Column(db.Date, nullable=False)

    patient = db.relationship("Patient", back_populates="visits")
    staff   = db.relationship("User",    back_populates="visits")
    orders  = db.relationship("Order",   back_populates="visit", cascade="all, delete-orphan")


# ---------- 4) 自由診療メニュー ----------
class Treatment(db.Model):
    __tablename__ = "treatments"

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer,    nullable=False)   # 税込み／抜きは後で調整
    note  = db.Column(db.String(256))

    order_items = db.relationship("OrderItem", back_populates="treatment")


# ---------- 5) オーダー ----------
class Order(db.Model):
    __tablename__ = "orders"

    id            = db.Column(db.Integer, primary_key=True)
    visit_id      = db.Column(db.Integer, db.ForeignKey("visits.id"), nullable=False)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"),  nullable=False)  # 会計担当
    created_at    = db.Column(db.Date, nullable=False)
    total_amount  = db.Column(db.Integer, default=0)
    payment_status= db.Column(db.String(20), default="unpaid")   # unpaid / paid
    note          = db.Column(db.String(256))

    visit   = db.relationship("Visit", back_populates="orders")
    cashier = db.relationship("User",  back_populates="orders")
    items   = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def recalc_total(self):
        self.total_amount = sum(item.subtotal for item in self.items)


# ---------- 6) オーダー明細 ----------
class OrderItem(db.Model):
    __tablename__ = "order_items"

    id           = db.Column(db.Integer, primary_key=True)
    order_id     = db.Column(db.Integer, db.ForeignKey("orders.id"),     nullable=False)
    treatment_id = db.Column(db.Integer, db.ForeignKey("treatments.id"), nullable=False)
    quantity     = db.Column(db.Integer, nullable=False, default=1)
    subtotal     = db.Column(db.Integer, nullable=False)

    order     = db.relationship("Order",     back_populates="items")
    treatment = db.relationship("Treatment", back_populates="order_items")

    def set_subtotal(self):
        self.subtotal = self.treatment.price * self.quantity
