import psycopg2
import os

def connect_db():
    DATABASE_URL = os.getenv("DATABASE_URL")

    conn = psycopg2.connect(DATABASE_URL)
    return conn


def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id SERIAL PRIMARY KEY,
        username TEXT,
        password TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()