from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    client_name = StringField('Вас зовут', [InputRequired(message="Введите имя!"),
                                            Length(min=1, message="Слишком короткая строка")])
    client_phone = StringField('Ваш телефон', [InputRequired(message="Введите телефон!"),
                                               Length(min=1, message="Слишком короткая строка")])
    client_weekday = HiddenField("day")
    client_time = HiddenField("time")
    teacher_id = HiddenField("teacher_id")