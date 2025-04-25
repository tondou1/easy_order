# app/__init__.py
import os
import pathlib
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# ────────────────────────────────────────────────────────────
# 環境変数読み込み
# ────────────────────────────────────────────────────────────
# app/ の一つ上の階層（プロジェクトルート）にある .env をロード
basedir = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(basedir / ".env")

# ────────────────────────────────────────────────────────────
# 拡張オブジェクト
# ────────────────────────────────────────────────────────────
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"   # 未ログイン時のリダイレクト先

# ────────────────────────────────────────────────────────────
# アプリファクトリ
# ────────────────────────────────────────────────────────────
def create_app() -> Flask:
    app = Flask(__name__)

    # ▼ Flask 設定
    # CSRF やセッションの署名に使う秘密鍵（.env の SECRET_KEY を優先）
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")

    # ── DB 接続先 ──
    # ローカル開発なら easy_order.db（SQLite）、本番では DATABASE_URL（PostgreSQL）を使う
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{basedir / 'easy_order.db'}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ▼ 拡張をアプリに紐付け
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ▼ モデルをインポート（Alembic 用）
    from . import models  # noqa: F401

    # ▼ Blueprint 登録
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)          # /login, /logout, /register

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)          # /

    from .patients import bp as patients_bp
    app.register_blueprint(patients_bp)

    from .visits import bp as visits_bp
    app.register_blueprint(visits_bp)

    from .treatments import bp as treatments_bp
    app.register_blueprint(treatments_bp)

    from .orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    return app
