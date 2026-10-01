#!/usr/bin/env bash
# Exit immediately on error
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static assets..."
python manage.py collectstatic --noinput

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Auto-seeding Deepak's portfolio data..."
python manage.py seed_portfolio

echo "==> Build completed successfully!"
