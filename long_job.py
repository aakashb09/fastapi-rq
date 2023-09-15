import requests

from db import get_db_connection


def count_words_at_url(url):
    response = requests.get(url)
    result = len(response.text.split())
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE jobs SET result = %s WHERE url = %s", (result, url))
    conn.commit()
    conn.close()
    return result
