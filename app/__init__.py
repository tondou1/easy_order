# app/__init__.py
import os
import pathlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

# ────────────────────────────────────────────────────────────
# 基本設定
# ────────────────────────────────────────────────────────────
basedir = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(basedir / ".env")          # .env を読み込む

db          = SQLAlchemy()
migrate     = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"   # 未ログイン時のリダイレクト先

# ────────────────────────────────────────────────────────────
# アプリファクトリ
# ────────────────────────────────────────────────────────────
def create_app() -> Flask:
    app = Flask(__name__)

    # ▼ Flask の設定
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + str(basedir / "easy_order.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ▼ 拡張を初期化
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ▼ モデルをインポート（Alembic が検知できるように）
    from . import models  # noqa: F401

    # ▼ Blueprint を登録
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)          # /login, /logout, /register

    from . import routes
    app.register_blueprint(routes.bp)        # /

    from .patients import bp as patients_bp
    app.register_blueprint(patients_bp)

    from .visits import bp as visits_bp
    app.register_blueprint(visits_bp)

    return app
