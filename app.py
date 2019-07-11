import os

from flask import (
    Flask, flash, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, current_user, login_user, login_required, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash
import json

try:
    app = Flask(__name__)

    app.config.from_object('config.DevelomentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
except Exception as e:
    print("Log: Error connecting Database.")

from api import currency_app
from models import currency, currency_rate, user
from models.currency import Currency
from models.user import Users

login_manager = LoginManager()
login_manager.login_view = 'render_login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    if not current_user.is_active:
        return render_template('login.html')
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def do_login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to
    # the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login data and try again.')
        return redirect(url_for('home'))

    login_user(user, remember=remember)
    return redirect(url_for('render_login'))


@app.route('/login', methods=['GET'])
def render_login():
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET'])
def render_signup_form():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def do_signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirm = request.form.get('confirm_password')

    user = Users.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('render_signup_form'))
    if password != password_confirm:
        flash('Error! The passwords does not match.')
        return redirect(url_for('render_signup_form'))

    new_user = Users(email=email, name=name, password=generate_password_hash(
        password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home'))


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
@login_required
def get_rate():
    iso_from = request.args.get('isoFrom')
    iso_to = request.args.get('isoTo')
    date = request.args.get('date')
    rate_obj = False

    if not iso_from or not iso_to or not date:
        currencies = Currency.find_all()
        return render_template(
            "get_rate_template.html", currencies=currencies)

    rate_obj = process_fetch_rate(iso_from, iso_to, date)

    return json.dumps(rate_obj.serialize())


@app.route("/convert")
@login_required
def convert():
    iso_from = request.args.get('isoFrom')
    iso_to = request.args.get('isoTo')
    date = request.args.get('date')
    amount = request.args.get('amount')
    rate_obj = False

    if not iso_from or not iso_to or not date or not amount:
        currencies = Currency.find_all()
        return render_template(
            "currency_covertion_template.html", currencies=currencies)

    rate_obj = process_fetch_rate(iso_from, iso_to, date)
    return json.dumps(rate_obj.rate * float(amount))


if __name__ == '__main__':
    app.run()
