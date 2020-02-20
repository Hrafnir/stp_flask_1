from flask import Flask, render_template 	# сперва подключим модуль
import data  # sample date from file
app = Flask(__name__) 	# объявим экземпляр фласка


@app.route('/')
def main():
    pass


if __name__ == '__main__':
    app.run(port=4999, debug=True)
