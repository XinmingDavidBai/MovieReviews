import psycopg2
import os
import time
import csv
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
            MovieId SERIAL PRIMARY KEY,
            MovieName TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Crew (
            CrewId SERIAL PRIMARY KEY ,
            CrewName TEXT NOT NULL,
            DirectMovieId int,
            FOREIGN KEY (DirectMovieId) REFERENCES Movies(MovieId)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Actors (
            CrewId int ,
            MovieId int,
            PRIMARY KEY (CrewID, MovieID),
            FOREIGN KEY (CrewId) REFERENCES Crew(CrewID),
            FOREIGN KEY (MovieId) REFERENCES MovieId(MovieId)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            UserId SERIAL PRIMARY KEY,
            UserName TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            ReviewId SERIAL PRIMARY KEY,
            Text TEXT,
            Rating int NOT NULL,
            MovieId int NOT NULL,
            UserId int NOT NULL,
            FOREIGN KEY (MovieId) REFERENCES Movies(MovieId),
            FOREIGN KEY (UserId) REFERENCES Users(UserId)
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
    path = "app/data/tmdb_5000_credits.csv"
    with open(path) as data_file:
        all_data = list(csv.reader(data_file))
        shaved_data = all_data[1:100]
        for row in shaved_data:
            movie_name = row[1].replace("'", "")
            try: 
                cur.execute("""
                    INSERT INTO Movies (MovieName) VALUES 
                """ + " ('" + movie_name + "');")
                print("Movie: " + movie_name + " seeded")
            except Exception as err:
                print(err)
    conn.commit()
    cur.close()
    conn.close()
    print("All movies seeded")


wait_for_db()
create_tables()
seed_movies()
