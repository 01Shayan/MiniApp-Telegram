# syntax=docker/dockerfile:1

FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    curl \
    gnupg \
    && apt-get clean

# Install Node.js (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Ensure theme folder is explicitly included
COPY theme/ /app/theme/

# Install Python dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Tailwind build step
WORKDIR /app/theme/static_src

# Install NPM dependencies
RUN npm install

# FIX: Install missing PostCSS plugin
RUN npm install autoprefixer

# Run Tailwind build
RUN npm run build

# Move back to root app directory
WORKDIR /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Production server using Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]