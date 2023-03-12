from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, EqualTo, InputRequired

class testform(FlaskForm):
    quest = RadioField('Answer', validators=[InputRequired('Выберите что-нибудь')], choices=[])
