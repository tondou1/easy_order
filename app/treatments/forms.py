from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class TreatmentForm(FlaskForm):
    name  = StringField("メニュー名",  validators=[DataRequired(), Length(max=64)])
    price = IntegerField("料金 (円)", validators=[DataRequired(), NumberRange(min=0)])
    note  = TextAreaField("メモ",      validators=[Length(max=256)])
    submit = SubmitField("保存")
