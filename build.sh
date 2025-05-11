#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

# Make sure to install these critical packages explicitly
echo "Installing additional critical packages..."
pip install psycopg2-binary gunicorn

# Create the initial database - force it to run with DATABASE_URL env var
echo "Initializing database..."
# Use a separate script that we can be sure runs correctly
echo "import os
import sys
from app import db, app, Cafe
from sqlalchemy import inspect

print('Running database initialization directly...')
with app.app_context():
    db.create_all()
    print('Tables created')
    inspector = inspect(db.engine)
    print('Tables in database:', inspector.get_table_names())
    
    # Add sample cafes if none exist
    if Cafe.query.count() == 0:
        print('Adding sample cafes...')
        sample_cafes = [
            Cafe(
                name='Starbucks',
                map_url='https://maps.app.goo.gl/XnSXDRhZK53gqHbL6',
                img_url='https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png',
                location='123 Main St, New York',
                has_sockets=True,
                has_toilet=True,
                has_wifi=True,
                can_take_calls=True,
                seats='30-40',
                coffee_price='$3.5'
            ),
            Cafe(
                name='Costa Coffee',
                map_url='https://maps.app.goo.gl/XnSXDRhZK53gqHbL6',
                img_url='https://upload.wikimedia.org/wikipedia/en/thumb/c/c7/Costa_Coffee_logo.svg/1200px-Costa_Coffee_logo.svg.png',
                location='456 Park Ave, New York',
                has_sockets=True,
                has_toilet=True,
                has_wifi=True,
                can_take_calls=False,
                seats='20-30',
                coffee_price='$3.0'
            ),
            Cafe(
                name='Blue Bottle',
                map_url='https://maps.app.goo.gl/XnSXDRhZK53gqHbL6',
                img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Blue_Bottle_Coffee_logo.svg/1200px-Blue_Bottle_Coffee_logo.svg.png',
                location='789 Broadway, New York',
                has_sockets=False,
                has_toilet=True,
                has_wifi=True,
                can_take_calls=True,
                seats='10-15',
                coffee_price='$4.0'
            )
        ]
        
        for cafe in sample_cafes:
            db.session.add(cafe)
        
        db.session.commit()
        print(f'Added {len(sample_cafes)} sample cafes')
    else:
        print(f'Database already has {Cafe.query.count()} cafes')
" > setup_db.py

python setup_db.py

# Also run the regular init_db.py as a fallback
python init_db.py || echo "Initialization with init_db.py failed, but continuing build process"

echo "Build completed successfully" 