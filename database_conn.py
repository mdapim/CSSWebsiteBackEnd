import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()
PASS = os.getenv('PASS')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
DBNAME = os.getenv('DBNAME')

def get_port():
    port = os.environ['PORT']
    return port

def get_db_user_connection():
    try:
        conn = psycopg2.connect(f"dbname={DBNAME} user=nspyhbjz host={HOST} port=5432 password={PASS}")
        return conn
    except:
        print("couldn't connect to server")


def db_select(conn ,query, parameters=()):
    if conn != None:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            try:
                cur.execute(query, parameters)
                data = cur.fetchall()
                conn.commit()
                return data            
            except:
                conn.reset()
                return "Error executing query."
    else:
        return "No connection"