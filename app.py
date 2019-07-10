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
def hello():
    isoFrom = request.args.get('isoFrom')
    isoTo = request.args.get('isoTo')
    date = request.args.get('date')

# crear la logica de este query en el model
    exist = currency_rate.CurrencyRate.query.filter(
        currency_rate.CurrencyRate.iso_code_to == isoTo,
        currency_rate.CurrencyRate.iso_code_from == isoFrom,
        currency_rate.CurrencyRate.date == date).first()
    if(exist is None):
        rate = currency_app.fetch_web_currency_rate(isoFrom, isoTo, date)
        newRate = currency_rate.CurrencyRate.insert_new_convertion_rate(
            isoTo, isoFrom, rate, date)
        return "hola Api, tu se creo la nueva converion: %6f" % newRate.rate
    else:
        return "Hola juanito esta es tu conversion %6f" % exist.rate


if __name__ == '__main__':
    app.run()
