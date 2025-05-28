from flask import Flask, render_template, request, jsonify
from .db import cur, conn
from .queries import search_movies, get_movie_rating, insert_review, get_common_actors

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

@app.route('/actors')
def in_common_actors():
    movie_id1 = request.args.get('movieId1', '').strip()
    movie_id2 = request.args.get('movieId2', '').strip()
    
    if movie_id1 and movie_id2:
        result = get_common_actors(movie_id1, movie_id2)
    else:
        result = []
    
    return jsonify(result)


