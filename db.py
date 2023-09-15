import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
    )
    return conn
