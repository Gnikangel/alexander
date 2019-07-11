import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

try:
    app = Flask(__name__)

    app.config.from_object('config.DevelomentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
except Exception as e:
    print("Log: Error connecting Database.")

from api import currency_app
from models import currency, currency_rate


@app.route("/")
def home():
    return render_template("index.html")


def process_fetch_rate(iso_from, iso_to, date):
    # crear la logica de este query en el model
    rate_obj = currency_rate.CurrencyRate.find_rate(
        iso_from, iso_to, date)

    if(rate_obj is None):
        rate = currency_app.fetch_web_currency_rate(iso_from, iso_to, date)
        rate_obj = currency_rate.CurrencyRate.insert_new_convertion_rate(
            iso_to, iso_from, rate, date)

    return rate_obj


@app.route("/getRate")
def get_rate():
    iso_from = request.args.get('isoFrom')
    iso_to = request.args.get('isoTo')
    date = request.args.get('date')
    rate_obj = False

    if not iso_from or not iso_to or not date:
        currencies = currency.Currency.find_all()
        return render_template(
            "get_rate_template.html", currencies=currencies)

    rate_obj = process_fetch_rate(iso_from, iso_to, date)

    return json.dumps(rate_obj.serialize())


@app.route("/convert")
def convert():
    iso_from = request.args.get('isoFrom')
    iso_to = request.args.get('isoTo')
    date = request.args.get('date')
    amount = request.args.get('amount')
    rate_obj = False

    if not iso_from or not iso_to or not date or not amount:
        currencies = currency.Currency.find_all()
        return render_template(
            "currency_covertion_template.html", currencies=currencies)

    rate_obj = process_fetch_rate(iso_from, iso_to, date)
    return json.dumps(rate_obj.rate * float(amount))


if __name__ == '__main__':
    app.run()
