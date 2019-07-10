from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('config.config.DevelomentConfig')
app.config['HOLA'] = False


@app.route("/")
def hello():
    return "Hola juanito como estas"


if __name__ == '__main__':
    app.run()
