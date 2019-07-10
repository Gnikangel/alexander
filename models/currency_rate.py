from pprint import pprint
from app import db


class CurrencyRate(db.Model):
    __tablename__ = 'currency_rate'

    currency_rate_id = db.Column(db.Integer, primary_key=True)
    iso_code_to = db.Column(db.String(3), nullable=False)
    iso_code_from = db.Column(db.String(3), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    rate = db.Column(db.Float(), nullable=False)

    def __init__(self, iso_code_to, iso_code_from, date, rate):
        self.iso_code_to = iso_code_to
        self.iso_code_from = iso_code_from
        self.date = date
        self.rate = rate

    def __repr__(self):
        return '<currency_rate_id {}>'.format(self.currency_rate_id)

    def serialize(self):
        return {
            'currency_rate_id': self.currency_rate_id,
            'iso_code_to': self.iso_code_to,
            'iso_code_from': self.iso_code_from,
            'date': self.date,
            'rate': self.rate,
        }

# Inserta el nuevo registro de conversion a la Base de datos
    def insert_new_convertion_rate(isoTo, isoFrom, rate, date):
        objToInsert = CurrencyRate(isoTo, isoFrom, date, rate)
        db.session.add(objToInsert)
        db.session.commit()
        pprint(objToInsert)
        return objToInsert
