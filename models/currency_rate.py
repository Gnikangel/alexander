
from app import db


class CurrencyRate(db.Model):
    __tablename__ = 'currency_rate'

    currency_rate_id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(3), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    rate = db.Column(db.Float(), nullable=False)

    def __init__(self, currency_rate_id, iso_code, date, rate):
        self.currency_rate_id = currency_rate_id
        self.iso_code = iso_code
        self.date = date
        self.rate = rate

    def __repr__(self):
        return '<currency_rate_id {}>'.format(self.currency_rate_id)

    def serialize(self):
        return {
            'currency_rate_id': self.currency_rate_id,
            'iso_code': self.iso_code,
            'date': self.date,
            'rate': self.rate,
        }
