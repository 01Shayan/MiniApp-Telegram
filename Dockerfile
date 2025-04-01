# syntax=docker/dockerfile:1

FROM python:3.11

# Install system dependencies and cron
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    curl \
    gnupg \
    cron \
    mysql-client \
    && apt-get clean

# Install Node.js (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Copy everything
COPY . .
COPY theme/ /app/theme/

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Tailwind build
WORKDIR /app/theme/static_src
RUN npm install && npm install autoprefixer && npm run build

# Back to root app dir
WORKDIR /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Setup cron job inside web container (runs every 5 mins)
RUN echo "*/5 * * * * cd /app && python manage.py sync_and_update_links >> /var/log/web-cron.log 2>&1" > /etc/cron.d/miniapp-cron && \
    chmod 0644 /etc/cron.d/miniapp-cron && \
    crontab /etc/cron.d/miniapp-cron && \
    touch /var/log/web-cron.log

# Start both cron and gunicorn
CMD service cron start && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 3