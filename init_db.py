import sqlite3
import os
import sys
from app import db, Cafe, User, Review, Like, app
import psycopg2

print("Initializing the database...")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print(f"cafes.db exists: {os.path.exists('cafes.db')}")

try:
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        print("Tables created successfully")
        
        # Print out all tables to verify
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        print("Tables in database:", inspector.get_table_names())
        
        # Check if cafes already imported
        if Cafe.query.count() == 0:
            print("No cafes found in database. Adding sample data...")
            
            # First, always try to import from cafes.db
            try:
                # Check in various locations where the file might be
                possible_paths = [
                    'cafes.db',
                    '/opt/render/project/src/cafes.db',
                    os.path.join(os.getcwd(), 'cafes.db')
                ]
                
                db_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        db_path = path
                        print(f"Found cafes.db at: {db_path}")
                        break
                
                if db_path:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM cafe")
                    cafes = cursor.fetchall()
                    
                    # Get column names
                    columns = [description[0] for description in cursor.description]
                    
                    # Import cafes
                    count = 0
                    for cafe_data in cafes:
                        cafe_dict = {columns[i]: cafe_data[i] for i in range(len(columns))}
                        
                        new_cafe = Cafe(
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
                        count += 1
                    
                    db.session.commit()
                    conn.close()
                    print(f"Successfully imported {count} cafes from SQLite database")
                else:
                    raise FileNotFoundError("cafes.db not found in any expected location")
            except Exception as e:
                print(f"Error importing from SQLite: {e}")
                print("Adding sample data instead...")
                
                # Add sample cafes if import fails
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
                    ),
                    Cafe(
                        name="Philz Coffee",
                        map_url="https://maps.app.goo.gl/XnSXDRhZK53gqHbL6",
                        img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Philz_Coffee_Logo.svg/1200px-Philz_Coffee_Logo.svg.png",
                        location="101 Market St, San Francisco",
                        has_sockets=True,
                        has_toilet=True,
                        has_wifi=True,
                        can_take_calls=True,
                        seats="25-35",
                        coffee_price="$3.8"
                    ),
                    Cafe(
                        name="Peet's Coffee",
                        map_url="https://maps.app.goo.gl/XnSXDRhZK53gqHbL6",
                        img_url="https://upload.wikimedia.org/wikipedia/en/thumb/a/a8/Peets_Coffee_logo.svg/1200px-Peets_Coffee_logo.svg.png",
                        location="503 Broadway, New York",
                        has_sockets=True,
                        has_toilet=True,
                        has_wifi=True,
                        can_take_calls=False,
                        seats="15-25",
                        coffee_price="$3.2"
                    )
                ]
                
                for cafe in sample_cafes:
                    db.session.add(cafe)
                    
                db.session.commit()
                print(f"Added {len(sample_cafes)} sample cafes to database")
        else:
            print(f"Database already contains {Cafe.query.count()} cafes. Skipping import.")

    print("Database initialization complete!")
    sys.exit(0)  # Exit successfully
except Exception as e:
    print(f"Error initializing database: {e}")
    sys.exit(1)  # Exit with error 