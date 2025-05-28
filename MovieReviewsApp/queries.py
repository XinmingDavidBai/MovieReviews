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

def get_movie_rating(movieId):
    cur = conn.cursor()
    cur.execute(
        "SELECT Movies.MovieId, Movies.MovieName, round(avg(Reviews.Rating), 1) "
        "FROM Movies "
        "LEFT JOIN Reviews ON Movies.MovieId = Reviews.MovieId "
        "WHERE Movies.MovieId = %s "
        "GROUP BY Movies.MovieId, Movies.MovieName",
        (movieId,)
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

def get_common_actors(movieId1, movieId2):
    cur = conn.cursor()
    cur.execute(
        "SELECT actors.CrewId, crew.crewname FROM actors "
        "LEFT JOIN crew ON crew.crewid = actors.crewid WHERE actors.MovieId = %s OR actors.MovieId = %s "
        "GROUP BY actors.crewId, crew.crewname HAVING COUNT(DISTINCT actors.MovieId) = 2", 
        (movieId1, movieId2)
    )
    crew = cur.fetchall()
    cur.close()

    return crew

