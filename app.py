import json
import data
from flask import Flask, render_template 	# сперва подключим модуль
import data  # sample date from file
app = Flask(__name__) 	# объявим экземпляр фласка



# @app.before_first_request
# def create_teachers_json():
#     print(data.teachers)

@app.route('/')
def main():
    pass


@app.route('/goals/<goal>/')
def get_goal():
    pass


@app.route('/profiles/<int:id_teacher>/')
def get_teacher(id_teacher):
    teach_dict = data.teachers[id_teacher]
    print(teach_dict)
    render_template('profile.html', teach_dict=teach_dict)


@app.route('/request/')
def do_request():
    pass


@app.route('/request_done/')
def req_done():
    pass


@app.route('/booking/<id_teacher>/<day>/<time>/')
def do_the_booking():
    pass


@app.route('/booking_done/')
def booking_done():
    pass


if __name__ == '__main__':
    app.run(port=4999, debug=True)
