from flask import Flask, render_template, request, jsonify
from .db import cur, conn
from .queries import search_movies

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    query = request.args.get('text', '').strip()
    results = search_movies(query) if query else []
    return jsonify(results)

