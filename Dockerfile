FROM python:3.11.5-slim-bullseye

WORKDIR /app
RUN apt-get update && apt-get -y install netcat gcc && apt-get clean
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
COPY . .

CMD ["/app/start.sh"]
