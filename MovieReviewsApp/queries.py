from .db import cur, conn
import re

def get_all_movies_with_rating():
    sql = """
    SELECT
        Movies.MovieId,
        Movies.MovieName,
        round(avg(Reviews.Rating), 1)
    FROM Movies
    LEFT JOIN Reviews ON Movies.MovieId = Reviews.MovieId
    GROUP BY Movies.MovieId, Movies.MovieName
    """
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

def movies_with_actors():
    sql = """
    SELECT
        Movies.MovieId,
        Movies.MovieName,
        STRING_AGG(Crew.CrewName, ', ') AS ActorList
    FROM Movies
    LEFT JOIN Actors ON Movies.MovieId = Actors.MovieId
    LEFT JOIN Crew ON Actors.CrewId = Crew.CrewId
    GROUP BY Movies.MovieId, Movies.MovieName
    """
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

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
    



