import psycopg2
from fastapi import Body, FastAPI
from redis import Redis
from rq import Queue

from long_job import count_words_at_url

app = FastAPI()
q = Queue(connection=Redis(host="redis", port=6379))


@app.on_event("startup")
def startup_event():
    print("Creating database if it doesn't exist")
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
    )
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            job_id text,
            url text,
            result text
        )
    """
    )
    conn.commit()
    conn.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def insert_job(job_id, url):
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
    )
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO jobs VALUES (%s, %s, %s)", (job_id, url, None))

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


@app.post("/start_task")
def start_task(url: str = Body(...)):
    job = q.enqueue(count_words_at_url, args=(url,))
    insert_job(job.id, url)
    return f"Task ({job.id}) added to queue at {job.enqueued_at}"


@app.get("/get_result/{job_id}")
def get_result(job_id: str):
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
    )
    c = conn.cursor()
    c.execute("SELECT result FROM jobs WHERE job_id = %s", (job_id,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return {"error": "No result found for this job id"}
    return {"result": result[0]}
