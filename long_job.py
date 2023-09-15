import requests

from db import DatabaseConnectionManager


def count_words_at_url(url):
    response = requests.get(url)
    result = len(response.text.split())
    with DatabaseConnectionManager() as conn:
        c = conn.cursor()
        c.execute("UPDATE jobs SET result = %s WHERE url = %s", (result, url))
        conn.commit()

    return result
