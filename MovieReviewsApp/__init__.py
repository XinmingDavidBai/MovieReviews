from flask import Flask, render_template, request, jsonify
from .db import cur, conn
from .queries import search_movies, get_movie_rating, insert_review

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    query = request.args.get('text', '').strip()
    results = search_movies(query) if query else []
    return jsonify(results)

@app.route('/review', methods=['POST'])
def add_review():
    data = request.get_json()
    insert_review(data)
    return jsonify({'success': True})

@app.route('/movie/<int:movie_id>')
def get_movie(movie_id):
    movie = get_movie_rating(movie_id)
    return jsonify(movie)



