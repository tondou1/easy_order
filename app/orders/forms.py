from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from ..models import Treatment

def treatment_choices():
    return [(t.id, f"{t.name}（¥{t.price}）") for t in Treatment.query.order_by(Treatment.name)]

class OrderItemForm(FlaskForm):
    treatment_id = SelectField("メニュー", coerce=int, validators=[DataRequired()])
    quantity     = IntegerField("数量",   default=1, validators=[DataRequired(), NumberRange(min=1)])
    submit       = SubmitField("追加")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.treatment_id.choices = treatment_choices()
