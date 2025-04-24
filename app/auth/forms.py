from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit   = SubmitField("ログイン")

class RegisterForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    role     = SelectField("権限", choices=[("admin", "管理者"), ("staff", "スタッフ")])
    submit   = SubmitField("ユーザー作成")
