FROM python:3.13-slim AS base

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency lock files
COPY requirements/ /app/requirements/

# Development stage
FROM base AS dev
RUN pip install --no-cache-dir -r /app/requirements/dev.txt
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base AS prod
RUN pip install --no-cache-dir -r /app/requirements/prod.txt
COPY . /app/
RUN mkdir -p /app/staticfiles /app/media
# Create non-root user and set permissions
RUN useradd -u 1000 django && chown -R django:django /app
USER django
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
