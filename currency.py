from datetime import datetime
from pprint import pprint

from lxml import etree
from requests import get

url_format = (
    'http://www.xe.com/currencytables/?from=%(currency_code)s&date=%(date)s')
today = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

try:
    fetched_data = get(url_format % {'currency_code': 'USD', 'date': today})
except:
    print("ERROR")

htmlelem = etree.fromstring(fetched_data.content, etree.HTMLParser())
rates_table = htmlelem.find(".//table[@id='historicalRateTbl']/tbody")
res = {}
for rate_entry in list(rates_table):
    if type(rate_entry) != etree._Comment:
        currency_code = rate_entry.find('.//a').text
        rate = float(rate_entry.find(
            "td[@class='historicalRateTable-rateHeader']").text)
        res[currency_code] = rate
