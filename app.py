import json
from flask import Flask, render_template, request  # сперва подключим модуль
import data  # sample date from file

app = Flask(__name__)  # объявим экземпляр фласка

days_name = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница"}


@app.route('/')
def main():
    return render_template('index.html', teachers=data.teachers)


@app.route('/goals/<goal>/')
def get_goal(goal):
    teachers_for_goal = []
    for teacher in data.teachers:
        if goal in teacher['goals']:
            teachers_for_goal.append(teacher)
    return render_template('goal.html', teachers=teachers_for_goal, goal= data.goals[goal])


@app.route('/profiles/<int:id_teacher>/')
def get_teacher(id_teacher):
    teach_dict = data.teachers[id_teacher]
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
    return render_template('request.html')


@app.route('/request_done/')
def req_done():
    pass


@app.route('/booking/<int:id_teacher>/<day>/<time>/')
def do_the_booking(id_teacher, day, time):
    day_ru = days_name[day]
    teach_dict = data.teachers[id_teacher]
    return render_template('booking.html',
                           teach_dict=teach_dict,
                           id_teacher=id_teacher,
                           day=day,
                           time=time,
                           day_ru=day_ru
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
                           )


if __name__ == '__main__':
    app.run(port=4999, debug=True)
