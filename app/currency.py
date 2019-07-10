from datetime import datetime
from pprint import pprint

from lxml import etree
from requests import get

isoDestino = 'MXN'
isoOrigen = 'USD'
amountToConvert = 16890.0863
rate = 1.0
fetched_data = False

url_format = (
    'http://www.xe.com/currencytables/?from=%(currency_code)s&date=%(date)s')
date = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

try:
    fetched_data = get(url_format % {'currency_code': isoOrigen, 'date': date})
except:
    print("Log -> ERROR al obtener las converciones")

if(fetched_data):
    htmlelem = etree.fromstring(fetched_data.content, etree.HTMLParser())
    rates_table = list(htmlelem.find(
        ".//table[@id='historicalRateTbl']/tbody"))
    filter = filter(lambda tr: type(tr) != etree._Comment, rates_table)
    rate = fetch_app_data(filter)
    rateRound = (round(rate, 6))
    pprint('Log -> Currency rate: %f' % rateRound)
    pprint('Log -> Amount to Convert: %f' % amountToConvert)
    pprint('Log -> Amount Converted: %f' % round(amountToConvert*rateRound, 6))
else:
    pprint('Log -> Currency rate: %f' % rate)


def fetch_app_data():
    for rate_entry in list(filter):
        currency_code = ''
        if(isoDestino == rate_entry.find('.//a').text):
            currency_code = rate_entry.find('.//a').text
            rate = float(rate_entry.find(
                "td[@class='historicalRateTable-rateHeader']").text)
