import sqlite3
import os
from app import db, Cafe, app
import psycopg2

print("Initializing the database...")

with app.app_context():
    # Create all tables
    db.create_all()
    print("Created database tables")
    
    # Check if cafes already imported
    if Cafe.query.count() == 0:
        print("Importing cafes from SQLite database...")
        try:
            # Connect to old database
            conn = sqlite3.connect('cafes.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cafe")
            cafes = cursor.fetchall()
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Import cafes
            for cafe_data in cafes:
                cafe_dict = {columns[i]: cafe_data[i] for i in range(len(columns))}
                
                new_cafe = Cafe(
                    id=cafe_dict['id'],
                    name=cafe_dict['name'],
                    map_url=cafe_dict['map_url'],
                    img_url=cafe_dict['img_url'],
                    location=cafe_dict['location'],
                    has_sockets=bool(cafe_dict['has_sockets']),
                    has_toilet=bool(cafe_dict['has_toilet']),
                    has_wifi=bool(cafe_dict['has_wifi']),
                    can_take_calls=bool(cafe_dict['can_take_calls']),
                    seats=cafe_dict['seats'],
                    coffee_price=cafe_dict['coffee_price']
                )
                db.session.add(new_cafe)
            
            db.session.commit()
            conn.close()
            print("Successfully imported cafes from SQLite database")
        except Exception as e:
            print(f"Error importing from SQLite: {e}")
            print("Adding sample data instead...")
            
            # Add a few sample cafes if SQLite import fails
            sample_cafes = [
                Cafe(
                    name="Starbucks",
                    map_url="https://maps.app.goo.gl/XnSXDRhZK53gqHbL6",
                    img_url="https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png",
                    location="123 Main St, New York",
                    has_sockets=True,
                    has_toilet=True,
                    has_wifi=True,
                    can_take_calls=True,
                    seats="30-40",
                    coffee_price="$3.5"
                ),
                Cafe(
                    name="Costa Coffee",
                    map_url="https://maps.app.goo.gl/XnSXDRhZK53gqHbL6",
                    img_url="https://upload.wikimedia.org/wikipedia/en/thumb/c/c7/Costa_Coffee_logo.svg/1200px-Costa_Coffee_logo.svg.png",
                    location="456 Park Ave, New York",
                    has_sockets=True,
                    has_toilet=True,
                    has_wifi=True,
                    can_take_calls=False,
                    seats="20-30",
                    coffee_price="$3.0"
                ),
                Cafe(
                    name="Blue Bottle",
                    map_url="https://maps.app.goo.gl/XnSXDRhZK53gqHbL6",
                    img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Blue_Bottle_Coffee_logo.svg/1200px-Blue_Bottle_Coffee_logo.svg.png",
                    location="789 Broadway, New York",
                    has_sockets=False,
                    has_toilet=True,
                    has_wifi=True,
                    can_take_calls=True,
                    seats="10-15",
                    coffee_price="$4.0"
                )
            ]
            
            for cafe in sample_cafes:
                db.session.add(cafe)
                
            db.session.commit()
            print("Added sample cafes to database")
    else:
        print("Database already contains cafes. Skipping import.")

print("Database initialization complete!") 