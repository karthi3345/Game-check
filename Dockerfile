# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (Postgres client, etc if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN playwright install chromium

# Copy project
COPY . /app/

# Create screenshots directory
RUN mkdir -p /app/screenshots
RUN chmod -R 777 /app/screenshots

# Start command (to be overridden in compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
