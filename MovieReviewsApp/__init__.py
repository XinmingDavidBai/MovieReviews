from flask import Flask, render_template, request, redirect, url_for
from .db import cur, conn
from .queries import get_all_movies_with_rating, movies_with_actors


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    query = request.args.get('query', '')
    results = []

    if query:
        cur.execute("SELECT Movies.MovieId, Movies.MovieName FROM Movies WHERE Movies.MovieName ILIKE %s", (f'%{query}%',))
        result = cur.fetchall()
        cur.close()
    
    return render_template("index.html", dquery=query, results=result)
