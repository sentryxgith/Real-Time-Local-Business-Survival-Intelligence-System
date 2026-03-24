import sqlite3
from config import DB_NAME

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating REAL,
        reviews INTEGER,
        price_level INTEGER,
        latitude REAL,
        longitude REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER,
        review_text TEXT,
        sentiment REAL,
        FOREIGN KEY (business_id) REFERENCES businesses(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()