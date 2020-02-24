import json
import random
from flask import Flask, render_template, request  # сперва подключим модуль
import data  # sample date from file

app = Flask(__name__)  # объявим экземпляр фласка

days_name = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница"}


# my first code reuse object ^_^
def select_teacher(id_teacher):
    for teach in data.teachers:
        if teach['id'] == id_teacher:
            return teach


@app.route('/')
def show_main_page():
    teachers = data.teachers
    random.shuffle(teachers)
    return render_template('index.html', teachers=teachers[:6])


@app.route('/tutors/')
def show_teachers():
    teachers = data.teachers
    return render_template('index.html', teachers=teachers, title='Все репетиторы')


@app.route('/goals/<goal>/')
def get_goal(goal):
    teachers_for_goal = []
    for teacher in data.teachers:
        if goal in teacher['goals']:
            teachers_for_goal.append(teacher)
    return render_template('goal.html', teachers=teachers_for_goal, goal= data.goals[goal])


@app.route('/profiles/<int:id_teacher>/')
def get_teacher(id_teacher):
    teach_dict = select_teacher(id_teacher)
    goals = []
    for i in teach_dict['goals']:
        goals.append(data.goals[i])
    return render_template('profile.html',
                           teach_dict=teach_dict,
                           title=teach_dict['name'],
                           goals=goals
                           )


@app.route('/request/')
def do_request():
    return render_template('request.html', title='Заявка на подбор')


@app.route('/request_done/', methods=['POST'])
def req_done():
    # catch all data from form
    request_dict = request.form
    with open('request.json', 'w') as req:
        json.dump(request_dict, req)
    # variable with value of goal from goals dict
    goal = data.goals[request_dict['goal']]
    return render_template('request_done.html',
                           request_dict=request_dict,
                           goal=goal,
                           title='Заявка создана, {}'.format(request_dict['name'])
                           )


@app.route('/booking/<int:id_teacher>/<day>/<time>/')
def do_the_booking(id_teacher, day, time):
    # variable with value of day on russian from days dict
    day_ru = days_name[day]
    teach_dict = select_teacher(id_teacher)
    return render_template('booking.html',
                           teach_dict=teach_dict,
                           id_teacher=id_teacher,
                           day=day,
                           time=time,
                           day_ru=day_ru,
                           title='Забронировать преподавателя'
                           )


@app.route('/booking_done/', methods=['POST'])
def show_booking_done():
    client_weekday = request.form['clientWeekday']
    client_time = request.form['clientTime']
    client_name = request.form['clientName']
    client_phone = request.form['clientPhone']
    with open('book.json', 'w') as file:
        data_book = {'client_weekday': client_weekday,
                     'client_time': client_time,
                     'client_name': client_name,
                     'client_phone': client_phone
                     }
        json.dump(data_book, file)
    return render_template('booking_done.html',
                           client_name=client_name,
                           client_phone=client_phone,
                           client_time=client_time,
                           client_weekday=days_name[client_weekday],
                           title='Преподаватель забронирован, {}'.format(client_name)
                           )


if __name__ == '__main__':
    app.run(port=4999, debug=True)
