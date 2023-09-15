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


class DatabaseConnectionManager:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = get_db_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
