FROM python:3.10-slim

ENV PYTHONUNBUFFERED TRUE

ENV WORKDIR /app

WORKDIR $WORKDIR

RUN apt-get update && apt-get install -y libgeos-dev

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP app/main.py

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "8082"]