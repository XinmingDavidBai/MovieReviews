from flask import Flask, render_template, request, redirect, url_for
from .db import cur, conn
from .queries import search_movies


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query', '').strip()
    results = search_movies(query) if query else []
    return render_template("index.html", query=query, results=results)
