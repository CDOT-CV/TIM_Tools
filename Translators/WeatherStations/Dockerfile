FROM python:3.10-slim

ENV PYTHONUNBUFFERED=TRUE

ENV WORKDIR=/app

WORKDIR $WORKDIR

COPY Translators/WeatherStations/ ./Translators/WeatherStations/

COPY Translators/Shared/ ./Translators/Shared/

ENV FLASK_APP=./Translators/WeatherStations/main.py

ENV PYTHONPATH="/app:${PYTHONPATH}"

RUN pip install -r ./Translators/WeatherStations/requirements.txt

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "8084"]