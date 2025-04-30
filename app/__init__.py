# app/__init__.py
import os
import pathlib
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# 環境変数読み込み
basedir = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(basedir / ".env")

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{basedir / 'easy_order.db'}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # モデルインポート（Alembic用）
    from . import models  # noqa: F401

    # Blueprint 登録
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    from .patients import bp as patients_bp
    app.register_blueprint(patients_bp)

    from .visits import bp as visits_bp
    app.register_blueprint(visits_bp)

    from .treatments import bp as treatments_bp
    app.register_blueprint(treatments_bp)

    from .orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    # ── ここで reports Blueprint を登録 ──
    from .reports import bp as reports_bp
    app.register_blueprint(reports_bp)

    return app
