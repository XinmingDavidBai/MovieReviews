from .db import cur, conn
import re

def search_movies(text):
    cur = conn.cursor()
    # Fetch all movies and average ratings (like get_all_movies_with_rating)
    cur.execute(
        "SELECT Movies.MovieId, Movies.MovieName, round(avg(Reviews.Rating), 1) "
        "FROM Movies "
        "LEFT JOIN Reviews ON Movies.MovieId = Reviews.MovieId "
        "GROUP BY Movies.MovieId, Movies.MovieName"
    )
    movies = cur.fetchall()
    cur.close()

    regex = re.compile(text, re.IGNORECASE)

    # Filter using regex on movie name
    return [movie for movie in movies if regex.search(movie[1])]

def get_movie_rating(movie_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT Movies.MovieId, Movies.MovieName, round(avg(Reviews.Rating), 1) "
        "FROM Movies "
        "LEFT JOIN Reviews ON Movies.MovieId = Reviews.MovieId "
        "WHERE Movies.MovieId = %s "
        "GROUP BY Movies.MovieId, Movies.MovieName",
        (movie_id,)
    )
    movie = cur.fetchone()
    cur.close()
    return movie

def insert_review(data):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Reviews (MovieId, Rating) VALUES (%s, %s)",
        (data['movieId'], data['rating'])
    )
    conn.commit()
    cur.close()

