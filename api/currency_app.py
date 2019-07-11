from datetime import datetime
from pprint import pprint

from lxml import etree
from requests import get
from models.currency_rate import CurrencyRate
from app import db


def fetch_app_data(fil, iso_to):
    rate = 1.0
    for rate_entry in list(fil):
        currency_code = ''
        if(iso_to == rate_entry.find('.//a').text):
            currency_code = rate_entry.find('.//a').text
            rate = float(rate_entry.find(
                "td[@class='historicalRateTable-rateHeader']").text)
    return round(rate, 6)


def fetch_web_currency_rate(iso_from, iso_to, date):
    rateRound = 1.0
    url_format = (
        'http://www.xe.com/currencytables/?'
        'from=%(currency_code)s&date=%(date)s')

    try:
        fetched_data = get(url_format % {
            'currency_code': iso_from, 'date': date})
    except Exception:
        print("Log -> ERROR al obtener las converciones")

    if(fetched_data):
        htmlelem = etree.fromstring(fetched_data.content, etree.HTMLParser())
        rates_table = list(htmlelem.find(
            ".//table[@id='historicalRateTbl']/tbody"))
        filtew = filter(lambda tr: type(tr) != etree._Comment, rates_table)
        rateRound = fetch_app_data(filtew, iso_to)
    else:
        pprint('Log -> Currency rate: %f' % rateRound)

    return rateRound
