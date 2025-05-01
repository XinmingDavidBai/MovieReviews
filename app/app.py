from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def hello():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from PostgreSQL!'")
    message = cur.fetchone()[0]
    conn.close()
    return message
