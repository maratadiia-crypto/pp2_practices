import psycopg2
from config import host, dbname, user, password, port

def connect():
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        return connection

    except Exception as error:
        print("Error while connecting to PostgreSQL")
        print(error)