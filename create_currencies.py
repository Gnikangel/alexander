from datetime import datetime
from lxml import etree
from requests import get
import psycopg2

connection = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432",
    database="alexander")

cr = connection.cursor()

currency_code = "USD"
date = datetime.strftime(datetime.now().date(), '%Y-%m-%d')

url_format = (
        'http://www.xe.com/currencytables/?'
        'from=%(currency_code)s&date=%(date)s')
try:
    fetched_data = get(url_format % {
        'currency_code': currency_code, 'date': date})
except Exception:
    print("Log -> ERROR al obtener las converciones")

htmlelem = etree.fromstring(fetched_data.content, etree.HTMLParser())
rates_table = htmlelem.find(".//table[@id='historicalRateTbl']/tbody")
res = {}
for rate_entry in list(rates_table):
    if type(rate_entry) != etree._Comment:
        currency_code = rate_entry.find('.//a').text
        currency_name = rate_entry.find(".//td[2]").text
        try:
            cr.execute(
                """INSERT INTO currency(iso_code, name, symbol)
                   VALUES('%s', '%s', '')""" % (
                    currency_code, currency_name.replace("'", "")))
            connection.commit()
        except Exception as e:
            print(currency_code)
            cr.close()
            cr = connection.cursor()
            pass
