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
python direct_db_fix.py

echo "Build completed successfully" 