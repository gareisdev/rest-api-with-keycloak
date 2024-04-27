FROM python:3.12.0-slim-bullseye

WORKDIR /app
EXPOSE 8080
CMD uvicorn app:app --host 0.0.0.0 --port 8080

COPY ./src/ .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
