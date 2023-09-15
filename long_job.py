import psycopg2
import requests


def count_words_at_url(url):
    response = requests.get(url)
    result = len(response.text.split())
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
    )
    c = conn.cursor()
    c.execute("UPDATE jobs SET result = %s WHERE url = %s", (result, url))
    conn.commit()
    conn.close()
    return result
