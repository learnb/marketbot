# Use an official Python base image based on Ubuntu 20.04 (focal) for good compatibility
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for Scrapy and other Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set workdir inside container
WORKDIR /app

# Copy requirements.txt separately to leverage Docker cache
COPY requirements.txt /app/

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Install python dependencies (including scrapy)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose Flask port (default 5000)
EXPOSE 5000

# Entrypoint command
CMD ["/app/entrypoint.sh"]