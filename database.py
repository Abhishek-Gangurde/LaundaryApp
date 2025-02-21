import sqlite3

def get_db_connection():
    conn = sqlite3.connect("laundry_service.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            service TEXT,
            status TEXT,
            pickup_datetime TEXT,
            notes TEXT,
            order_time TEXT
        )
    ''')
    conn.commit()
    return conn
