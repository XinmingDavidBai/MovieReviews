from .db import cur, conn

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

def search_movies(query):
    cur = conn.cursor()
    cur.execute(
        "SELECT movieid, moviename FROM movies WHERE moviename ILIKE %s",
        (f"%{query}%",)
    )
    results = cur.fetchall()
    cur.close()
    return results


