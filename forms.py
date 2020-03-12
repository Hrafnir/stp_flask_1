from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    client_name = StringField('Вас зовут', [InputRequired(), Length(min=1)])
    client_phone = StringField('Ваш телефон', [InputRequired(), Length(min=1)])