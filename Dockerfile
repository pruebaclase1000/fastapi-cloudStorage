# FROM python:3.9-buster
FROM python:3.10-slim

ENV PYTHONUNBIFFERED True

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# EXPONER EL PUERTO
ENV PORT=80
EXPOSE $PORT

COPY . ./

CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}