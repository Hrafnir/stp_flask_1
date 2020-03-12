import json
import random
from flask import Flask, render_template, request  # сперва подключим модуль
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField
import data  # sample date from file

app = Flask(__name__)  # объявим экземпляр фласка
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

app.secret_key = 'asdwefwedf'
migrate = Migrate(app, db)

days_name = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница",
             "sat": "Суббота", "sun": "Воскресенье"}


# # my first code reuse function object ^_^
# def select_teacher(id_teacher):
#     for teach in data.teachers:
#         if teach['id'] == id_teacher:
#             return teach


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


# teacher = Teacher(t_id=1231213323434,
#                   name="asdf",
#                   about='asdfasdf',
#                   rating=4.5,
#                   picture='sadf',
#                   price=234,
#                   goals='[asdf,asdf]',
#                   free="{asdf:asdfasdf}"
#                   )
# db.session.add(teacher)
# db.session.commit()


class Booking(db.Model):
    __tablename__ = 'bookings'
    b_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    client_weekday = db.Column(db.String, nullable=False)
    client_time = db.Column(db.Time, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.t_id"))
    teacher = db.relationship("Teacher", back_populates="bookings")


class Request(db.Model):
    __tablename__ = 'requests'
    r_id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)


# @app.route('/')
# def show_main_page():
#     teachers = data.teachers
#     random.sample(teachers, 6)
#     return render_template('index.html', teachers=teachers)
#
#
# @app.route('/tutors/')
# def show_teachers():
#     teachers = data.teachers
#     return render_template('index.html', teachers=teachers, title='Все репетиторы')
#
#
#need to add goal url in Goal model
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
#
#
# @app.route('/request/')
# def do_request():
#     return render_template('request.html', title='Заявка на подбор')
#
#
# @app.route('/request_done/', methods=['POST'])
# def req_done():
#     # catch all data from form
#     request_dict = request.form
#     with open('request.json', 'w') as req:
#         json.dump(request_dict, req)
#     # variable with value of goal from goals dict
#     goal = data.goals[request_dict['goal']]
#     return render_template('request_done.html',
#                            request_dict=request_dict,
#                            goal=goal,
#                            title='Заявка создана, {}'.format(request_dict['name'])
#                            )
#
#
# @app.route('/booking/<int:id_teacher>/<day>/<time>/')
# def do_the_booking(id_teacher, day, time):
#     # variable with value of day on russian from days dict
#     day_ru = days_name[day]
#     teach_dict = select_teacher(id_teacher)
#     return render_template('booking.html',
#                            teach_dict=teach_dict,
#                            id_teacher=id_teacher,
#                            day=day,
#                            time=time,
#                            day_ru=day_ru,
#                            title='Забронировать преподавателя'
#                            )
#
#
# @app.route('/booking_done/', methods=['POST'])
# def show_booking_done():
#     client_weekday = request.form['clientWeekday']
#     client_time = request.form['clientTime']
#     client_name = request.form['clientName']
#     client_phone = request.form['clientPhone']
#     with open('book.json', 'w') as file:
#         data_book = {'client_weekday': client_weekday,
#                      'client_time': client_time,
#                      'client_name': client_name,
#                      'client_phone': client_phone
#                      }
#         json.dump(data_book, file)
#     return render_template('booking_done.html',
#                            client_name=client_name,
#                            client_phone=client_phone,
#                            client_time=client_time,
#                            client_weekday=days_name[client_weekday],
#                            title='Преподаватель забронирован, {}'.format(client_name)
#                            )

db.create_all()
if __name__ == '__main__':
    app.run(port=4999, debug=True)
