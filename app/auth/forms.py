# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
class LoginForm(FlaskForm):
    login_id = StringField("ログインID", validators=[DataRequired(), Length(max=64)])
    password = PasswordField(
        "パスワード", validators=[DataRequired()]
    )
    submit = SubmitField("ログイン")

class RegisterForm(FlaskForm):
    login_id  = StringField("ログインID",   validators=[DataRequired(), Length(max=64)])
    name      = StringField("ユーザー名",   validators=[DataRequired(), Length(max=64)])
    role      = SelectField("権限",       choices=[("admin","管理者"),("staff","スタッフ")], validators=[DataRequired()])
    password = PasswordField(
        "パスワード", validators=[DataRequired()]
    )
    password2 = PasswordField(
        "パスワード（確認）",
        validators=[
            DataRequired(),
            EqualTo("password", message="パスワードが一致しません")
        ]
    )
    submit = SubmitField("ユーザー作成")
