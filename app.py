import json
import random
from flask import Flask, render_template, request  # сперва подключим модуль
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)  # объявим экземпляр фласка
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

app.secret_key = 'asdwefwedf'
migrate = Migrate(app, db)

days_name = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница",
             "sat": "Суббота", "sun": "Воскресенье"}


def get_goals():
    goals = dict()
    for goal in db.session.query(Goal).all():
        if len(goals) <= 4:  # 4 may be variable for main page's limit of goals
            goals[goal.goal_url] = goal.goal_name
        else:
            break
    return goals


# db models


class Teacher(db.Model):
    __tablename__ = 'teachers'
    t_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.relationship("Goal", back_populates="teacher")
    free = db.Column(db.String, nullable=False)
    bookings = db.relationship("Booking", back_populates="teacher")


class Goal(db.Model):
    __tablename__ = 'goals'
    g_id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String, nullable=False)
    goal_url = db.Column(db.String, nullable=False)
    teacher = db.relationship("Teacher", back_populates="goals")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.t_id"))


class Booking(db.Model):
    __tablename__ = 'bookings'
    b_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    client_weekday = db.Column(db.String, nullable=False)
    client_time = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.t_id"))
    teacher = db.relationship("Teacher", back_populates="bookings")


class Request(db.Model):
    __tablename__ = 'requests'
    r_id = db.Column(db.Integer, primary_key=True)
    client_goal = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    free_time = db.Column(db.String, nullable=False)


# forms objects


class BookingForm(FlaskForm):
    client_name = StringField('Вас зовут', [InputRequired(message="Введите имя!"),
                                            Length(min=1, message="Слишком короткая строка")])
    client_phone = StringField('Ваш телефон', [InputRequired(message="Введите телефон!"),
                                               Length(min=1, message="Слишком короткая строка")])
    client_weekday = HiddenField("day")
    client_time = HiddenField("time")
    teacher_id = HiddenField("teacher_id")


class RequestForm(FlaskForm):
    client_name = StringField('Вас зовут', [InputRequired(message="Введите имя!"),
                                            Length(min=1, message="Слишком короткая строка")])
    client_phone = StringField('Ваш телефон', [InputRequired(message="Введите телефон!"),
                                               Length(min=1, message="Слишком короткая строка")])
    goals = []
    for key, value in get_goals().items():
        goals.append((key, value))
    client_goal = RadioField('Какая цель ваших занятий?', choices=goals)
    free_time = RadioField('Сколько свободного времени у вас есть?',
                           choices=[("1-2", "1-2 часа в неделю"), ("3-5", "3-5 часов в неделю"),
                                    ("5-7", "5-7 часов в неделю"), ("7-10", "7-10 часов в неделю")])


@app.route('/')
def show_main_page():
    teachers = db.session.query(Teacher).all()
    teach_s = random.sample(teachers, 6)
    goals = get_goals()
    return render_template('index.html',
                           teachers=teach_s,
                           goals=goals
                           )


@app.route('/tutors/')
def show_teachers():
    teachers = db.session.query(Teacher).all()
    goals = get_goals()
    return render_template('index.html',
                           teachers=teachers,
                           title='Все репетиторы',
                           goals=goals
                           )


@app.route('/goals/<goal>/')
def get_goal(goal):
    teachers_for_goal = db.session.query(Goal).filter(Goal.goal_url == goal).all()
    teachers = []
    for teacher in teachers_for_goal:
        teachers.append(db.session.query(Teacher).get(teacher.teacher_id))
    goal_name = db.session.query(Goal).filter(Goal.goal_url == goal).first().goal_name
    return render_template('goal.html', teachers=teachers, goal=goal_name)


@app.route('/profiles/<int:id_teacher>/')
def get_teacher(id_teacher):
    teacher = db.session.query(Teacher).get(id_teacher)
    if teacher:
        goals = db.session.query(Goal).filter(Goal.teacher_id == id_teacher).all()
        goals_for_teacher = []
        for i in goals:
            goals_for_teacher.append(i.goal_name)
        free_dict = json.loads(teacher.free)
        return render_template('profile.html',
                               teach_dict=teacher,
                               title=teacher.name,
                               goals=goals_for_teacher,
                               free_dict=free_dict,
                               days_name=days_name
                               )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Страница не найдена'), 404


@app.route('/request/')
def do_request():
    form = RequestForm()
    return render_template('request.html', title='Заявка на подбор', form=form)


@app.route('/request_done/', methods=['POST', 'GET'])
def req_done():
    if request.method == 'POST':
        form = RequestForm()
        goal = get_goals()[form.client_goal.data]
        if form.validate():
            write_req = Request()
            form.populate_obj(write_req)
            db.session.add(write_req)
            db.session.commit()
            return render_template('request_done.html',
                                   form=form,
                                   goal=goal,
                                   title='Заявка создана, {}'.format(form.client_name)
                                   )
    else:
        return "Кажется, форма не отправлена!"


@app.route('/booking/<int:id_teacher>/<day>/<b_time>/')
def do_the_booking(id_teacher, day, b_time):
    # variable with value of day on russian from days dict
    day_ru = days_name[day]
    form = BookingForm(client_weekday=day,
                       client_time=b_time,
                       teacher_id=id_teacher
                       )
    teach_dict = db.session.query(Teacher).get(id_teacher)
    return render_template('booking.html',
                           teach_dict=teach_dict,
                           day_ru=day_ru,
                           form=form,
                           title='Забронировать преподавателя'
                           )


@app.route('/booking_done/', methods=['POST', 'GET'])
def show_booking_done():
    if request.method == 'POST':
        form = BookingForm()
        day_ru = days_name[form.client_weekday.data]
        if form.validate():
            book = Booking()
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            return render_template('booking_done.html',
                                   info=form,
                                   day_ru=day_ru,
                                   title='Преподаватель забронирован'
                                   )
        else:
            return "Форма получена, но есть ошибки!"
    else:
        return "Кажется, форма не отправлена!"


db.create_all()
if __name__ == '__main__':
    app.run(port=4999, debug=True)
