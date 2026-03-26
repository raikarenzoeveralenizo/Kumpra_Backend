# Dockerfile (Django REST API)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
 PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
 gcc \
 libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . /app/

EXPOSE 8000

# Run with Gunicorn (recommended for production)
# Set your WSGI path below (example: config.wsgi:application)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
