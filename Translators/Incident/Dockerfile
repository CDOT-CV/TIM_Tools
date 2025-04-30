FROM python:3.10-slim

ENV PYTHONUNBUFFERED=TRUE

ENV WORKDIR=/app

WORKDIR $WORKDIR

COPY Translators/Incident/ ./Translators/Incident/

COPY Translators/Shared/ ./Translators/Shared/

ENV FLASK_APP=./Translators/Incident/main.py

ENV PYTHONPATH="/app:${PYTHONPATH}"

RUN apt-get update && apt-get install -y libgeos-dev

RUN pip install -r ./Translators/Incident/requirements.txt

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "8083"]