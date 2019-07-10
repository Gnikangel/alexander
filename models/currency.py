
from app import db


class Currency(db.Model):
    __tablename__ = 'currency'

    currency_id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    symbol = db.Column(db.String(), nullable=False)

    def __init__(self, currency_id, iso_code, name, symbol):
        self.currency_id = currency_id
        self.iso_code = iso_code
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return '<currency_id {}>'.format(self.currency_id)

    def serialize(self):
        return {
            'currency_id': self.currency_id,
            'iso_code': self.iso_code,
            'name': self.name,
            'symbol': self.symbol,
        }
