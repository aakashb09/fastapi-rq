import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnectionManager:
    def __init__(self):
        self.conn = None

    def get_db_connection(self):
        conn = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db",
            port="5432",
        )
        return conn

    def __enter__(self):
        self.conn = self.get_db_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
