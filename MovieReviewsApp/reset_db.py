import psycopg2
import os
import time

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

def reset_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    try:   
        cur.execute("""
            DROP TABLE Movies, Crew, Actors, Reviews;
        """)
    except Exception as err:
        print(err)
        cur.close()
        conn.close()
        return
    conn.commit()
    cur.close()
    conn.close()
    print("All tables dropped")

wait_for_db()
reset_db()