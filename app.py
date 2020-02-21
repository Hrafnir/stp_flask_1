import json
import data
from flask import Flask, render_template 	# сперва подключим модуль
import data  # sample date from file
app = Flask(__name__) 	# объявим экземпляр фласка



@app.route('/')
def main():
    pass


@app.route('/goals/<goal>/')
def get_goal():
    pass


@app.route('/profiles/<int:id_teacher>/')
def get_teacher(id_teacher):
    teach_dict = data.teachers[id_teacher]
    goals = []
    for i in teach_dict['goals']:
        goals.append(data.goals[i])
    return render_template('profile.html', teach_dict=teach_dict, title=teach_dict['name'], goals=goals)


@app.route('/request/')
def do_request():
    pass


@app.route('/request_done/')
def req_done():
    pass


@app.route('/booking/<int:id_teacher>/<day>/<time>/')
def do_the_booking(id_teacher, day, time):
    days_name = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница"}
    day_ru = days_name[day]
    teach_dict = data.teachers[id_teacher]
    return render_template('booking.html', teach_dict=teach_dict, id_teacher=id_teacher, day=day, time=time, day_ru=day_ru)


@app.route('/booking_done/')
def booking_done():
    pass


if __name__ == '__main__':
    app.run(port=4999, debug=True)
