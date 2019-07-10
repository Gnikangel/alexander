import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
try:
    app = Flask(__name__)

    app.config.from_object('config.DevelomentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
except Exception as e:
    print("Log: Error connecting Database.")

from models import currency, currency_rate


@app.route("/")
def hello():
    return "Hola juanito como estas"


if __name__ == '__main__':
    app.run()
