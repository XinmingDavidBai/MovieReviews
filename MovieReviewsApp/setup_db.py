import psycopg2
import os
import time
import csv
import json
from dotenv import load_dotenv

load_dotenv()
def wait_for_db():
    for _ in range(10):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            conn.close()
            return
        except:
            time.sleep(1)
    raise Exception("Database not available")
def create_tables():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            MovieId int PRIMARY KEY,
            MovieName TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Crew (
            CrewId int PRIMARY KEY ,
            CrewName TEXT NOT NULL,
            DirectMovieId int,
            FOREIGN KEY (DirectMovieId) REFERENCES Movies(MovieId)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Actors (
            CrewId int ,
            MovieId int,
            PRIMARY KEY (MovieId, CrewId),
            FOREIGN KEY (CrewId) REFERENCES Crew(CrewID),
            FOREIGN KEY (MovieId) REFERENCES Movies(MovieId)
        );
    """)
    #cur.execute("""
    #    CREATE TABLE IF NOT EXISTS Users (
    #        UserId SERIAL PRIMARY KEY,
    #        UserName TEXT UNIQUE NOT NULL,
    #        Password TEXT NOT NULL
    #    );
    #""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            ReviewId SERIAL PRIMARY KEY,
            Text TEXT,
            Rating int NOT NULL,
            MovieId int NOT NULL,
            FOREIGN KEY (MovieId) REFERENCES Movies(MovieId)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created.")
def seed_movies():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    path = "MovieReviewsApp/data/tmdb_5000_credits.csv"
    with open(path) as data_file:
        all_data = list(csv.reader(data_file))
        shaved_data = all_data[1:100]
        for row in shaved_data:
            movie_id = row[0]
            movie_name = row[1].replace("'", "") #postgres doesnt allow that symbol
            # seed movie
            try: 
                cur.execute("""
                    INSERT INTO Movies (MovieId,MovieName) VALUES 
                """ + " (" + movie_id + ",'" + movie_name + "');")
                print("Movie: " + movie_name + " seeded")
            except Exception as err:
                print(err)
                cur.close()
                conn.close()
                return
            # seed actors 
            crew = row[2]
            crew_json = json.loads(crew)
            for c in crew_json:
                crew_id = str(c["id"])
                crew_name = str(c["name"]).replace("'",'')
                try: 
                    cur.execute("""
                        INSERT INTO Crew (CrewId, CrewName) SELECT 
                    """ + " " + crew_id + ",'" + crew_name + "' "
                    "WHERE NOT EXISTS (SELECT CrewId FROM Crew WHERE CrewId = " + crew_id + ");")
                    cur.execute("""
                        INSERT INTO Actors (MovieId, CrewId) SELECT 
                    """ + " " + movie_id + ",'" + crew_id + "' "
                    "WHERE NOT EXISTS (SELECT MovieId,CrewId FROM Actors WHERE CrewId = " + crew_id + " AND MovieId = " + movie_id + ");")
                except Exception as err:
                    print(err)
                    cur.close()
                    conn.close()
                    return
            # seed director
            crew = row[3]
            crew_json = json.loads(crew)
            for c in crew_json:
                job = str(c["job"])
                if (job != "Director"):
                    continue
                crew_id = str(c["id"])
                crew_name = str(c["name"]).replace("'",'')
                try:
                    cur.execute("""
                        INSERT INTO Crew (CrewId, CrewName) SELECT 
                    """ + " " + crew_id + ",'" + crew_name + "' "
                    "WHERE NOT EXISTS (SELECT CrewId FROM Crew WHERE CrewId = " + crew_id + ");")
                    cur.execute("""
                        UPDATE Crew
                        SET DirectMovieId = 
                    """ + movie_id + " WHERE CrewId = " + crew_id + ";")
                except Exception as err:
                    print(err)
                    cur.close()
                    conn.close()
                    return
    conn.commit()
    cur.close()
    conn.close()
    print("All movies seeded")


wait_for_db()
create_tables()
seed_movies()

