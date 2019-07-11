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

from api import currency_app
from models import currency, currency_rate


@app.route("/getRate")
def get_rate():
    iso_from = request.args.get('isoFrom')
    iso_to = request.args.get('isoTo')
    date = request.args.get('date')

    # crear la logica de este query en el model
    exist = currency_rate.CurrencyRate.find_rate(
        iso_from, iso_to, date)

    if(exist is None):
        rate = currency_app.fetch_web_currency_rate(iso_from, iso_to, date)
        newRate = currency_rate.CurrencyRate.insert_new_convertion_rate(
            iso_to, iso_from, rate, date)
        return "hola Api, tu se creo la nueva converion: %6f" % newRate.rate
    else:
        return "Hola juanito esta es tu conversion %6f" % exist.rate


if __name__ == '__main__':
    app.run()
