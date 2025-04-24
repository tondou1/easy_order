from datetime import date
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from ..models import Patient

def patient_choices():
    # 動的にプルダウンを更新
    return [(p.id, f"{p.chart_number} : {p.name}") for p in Patient.query.order_by(Patient.chart_number)]

class VisitForm(FlaskForm):
    patient_id = SelectField("患者", coerce=int, validators=[DataRequired()])
    visit_date = DateField("来院日", default=date.today, format="%Y-%m-%d")
    submit     = SubmitField("保存")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_id.choices = patient_choices()
