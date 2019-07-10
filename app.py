from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('config.config.DevelomentConfig')
app.config['HOLA'] = False
#db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
