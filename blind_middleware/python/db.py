import sqlite3

def send_query(query) -> bool:
    with sqlite3.connect("./database.db") as db:
        try:
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
        except sqlite3.OperationalError as e:
            print(f"{query}: {e}")
            return False
    
    return True

initial_query_1 = """
CREATE TABLE IF NOT EXISTS logger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT,
    user_agent TEXT,
    referer TEXT,
    url TEXT,
    cookie TEXT,
    created_at TEXT
);
"""

initial_query_2 = """
CREATE TABLE IF NOT EXISTS flag (
    id INTEGER PRIMARY KEY UNIQUE,
    secret TEXT NOT NULL UNIQUE
);
"""

initial_query_3 = """
INSERT INTO flag (id, secret) VALUES (1, 'KCSC{ehehe}');
"""

assert(send_query(initial_query_1))
assert(send_query(initial_query_2))
assert(send_query(initial_query_3))