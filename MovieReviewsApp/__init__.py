from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# Connect to the database
conn = psycopg2.connect(database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                        password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port= os.getenv("DB_PORT"))

# create a cursor
cur = conn.cursor()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", data = get_all_movies())

def get_all_movies():
    sql = """
    SELECT * FROM Movies
    """
    cur.execute(sql)
    movies = cur.fetchall()
    cur.close()
    return movies
