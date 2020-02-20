from flask import Flask, render_template 	# сперва подключим модуль
import data  # sample date from file
app = Flask(__name__) 	# объявим экземпляр фласка


@app.route('/')
def main():
    pass


@app.route('/goals/<goal>/ ')
def get_goal():
    pass


@app.route('/profiles/<id tutor>/ ')
def get_tutor():
    pass


@app.route('/request/')
def do_request():
    pass


@app.route('/request_done/')
def req_done():
    pass


@app.route('/booking/<id учителя>/<день недели>/<время>/')
def do_the_booking():
    pass

@app.route('/booking_done/ ')
def booking_done():
    pass


if __name__ == '__main__':
    app.run(port=4999, debug=True)
