#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create the initial database if it doesn't exist
python init_db.py 