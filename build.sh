#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

# Make sure to install these critical packages explicitly
echo "Installing additional critical packages..."
pip install psycopg2-binary gunicorn

# Create the initial database
echo "Initializing database..."
python init_db.py || echo "Database initialization failed, but continuing build process"

echo "Build completed successfully" 