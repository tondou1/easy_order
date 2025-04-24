from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class PatientForm(FlaskForm):
    chart_number = StringField("カルテ番号", validators=[DataRequired(), Length(max=20)])
    name         = StringField("氏名",       validators=[DataRequired(), Length(max=64)])
    furigana     = StringField("フリガナ",   validators=[Optional(),  Length(max=64)])
    birth_date   = DateField("生年月日",     validators=[Optional()], format="%Y-%m-%d")
    gender       = SelectField("性別", choices=[("男", "男"), ("女", "女"), ("その他", "その他")])
    emergency_contact = StringField("緊急連絡先", validators=[Optional(), Length(max=64)])
    submit       = SubmitField("保存")
