from flask import Flask, request
from datetime import datetime
import json
import sqlite3

def send_query(query) -> bool:
    with sqlite3.connect("./database.db") as db:
        try:
            cursor = db.cursor()
            print(cursor.execute(query))
            db.commit()
        except sqlite3.OperationalError as e:
            print(f"{query}: {e}")
            return False
    
    return True

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    all_cookies ="; ".join(f"{key}={value}" for key, value in request.cookies.items())
    
    ip_address = request.remote_addr
    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")
    url = request.url
    cookie = None if len(all_cookies) == 0 else all_cookies
    created_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
    
    # print (f"***\n{ip_address} \n{user_agent} \n{referer} \n{url} \n{cookie} \n{created_at}\n***")
    
    query = f"INSERT INTO logger (ip_address, user_agent, referer, url, cookie, created_at) VALUES ('{ip_address}', '{user_agent}', '{referer}', '{url}', '{cookie}', '{created_at}')"
    
    return "Logged" if send_query(query) else "Error"
    

if __name__ == "__name__":
    app.run(port=3000, threaded=True)
    
# flask --app server run --port=3000