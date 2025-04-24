from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os, pathlib

basedir = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(basedir / '.env')          # .env を読み込む

db  = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'     # 未ログイン時リダイレクト先

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(basedir / 'easy_order.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 拡張を初期化
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ルート登録
    from . import routes
    app.register_blueprint(routes.bp)

    return app
