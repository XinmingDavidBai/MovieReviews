from .db import cur

# SELECT
#   Movies.MovieId,
#   Movies.MovieName,
#   STRING_AGG(Crew.CrewName, ', ') AS ActorList
# FROM Movies
# LEFT JOIN Actors ON Movies.MovieId = Actors.MovieId
# LEFT JOIN Crew ON Actors.CrewId = Crew.CrewId
# GROUP BY Movies.MovieId, Movies.MovieName;


def get_all_movies():
    sql = """
    SELECT * FROM Movies
    """
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    return res

