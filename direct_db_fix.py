import os
from app import app, db, Cafe

# List of cafes from cafes.db
CAFE_DATA = [
    {
        "name": "Science Gallery London",
        "map_url": "https://g.page/scigallerylon?share",
        "img_url": "https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg",
        "location": "London Bridge",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": False,
        "can_take_calls": True,
        "seats": "50+",
        "coffee_price": "£2.40"
    },
    {
        "name": "Social - Copeland Road",
        "map_url": "https://g.page/CopelandSocial?share",
        "img_url": "https://images.squarespace-cdn.com/content/v1/5734f3ff4d088e2c5b08fe13/1555848382269-9F13FE1WQDNUUDQOAOXF/ke17ZwdGBToddI8pDm48kAeyi0pcxjZfLZiASAF9yCBZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpzV8NE8s7067ZLWyi1jRvJklJnlBFEUyq1al9AqaQ7pI4DcRJq_Lf3JCtFMXgpPQyk/copeland-park-bar-peckham",
        "location": "Peckham",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "20-30",
        "coffee_price": "£2.75"
    },
    {
        "name": "One & All Cafe Peckham",
        "map_url": "https://g.page/one-all-cafe?share",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipOMzXpKAQNyUvrjTGHqCgWk8spwnzwP8Ml2aDKt=s0",
        "location": "Peckham",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "20-30",
        "coffee_price": "£2.75"
    },
    {
        "name": "Old Spike",
        "map_url": "https://www.google.com/maps/place/Old+Spike+Roastery/@51.4651552,-0.0666088,17z/data=!4m12!1m6!3m5!1s0x487603a3a7dd838d:0x4105b39b30a737cf!2sOld+Spike+Roastery!8m2!3d51.4651552!4d-0.0666088!3m4!1s0x487603a3a7dd838d:0x4105b39b30a737cf!8m2!3d51.4651552!4d-0.0666088",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipPBAt6bYna7pv5c7e_PhCDPMKPb6oFf6kMT2VQ1=s0",
        "location": "Peckham",
        "has_sockets": True,
        "has_toilet": False,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "0-10",
        "coffee_price": "£2.80"
    },
    {
        "name": "Fuckoffee Bermondsey",
        "map_url": "https://goo.gl/maps/ugP2B1AV7FELHSgn6",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipM9Dz_QMkOF2da1aNLuTzS_vPvVWBnE84rZLK_G=s0",
        "location": "Bermondsey",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "20-30",
        "coffee_price": "£2.65"
    },
    {
        "name": "Mare Street Market",
        "map_url": "https://goo.gl/maps/DWnwaeeiwdYsBkEH9",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipN-C650VmJ1XZhzOIBTg1bUu3_to_GHpyrmUplt=s0",
        "location": "Hackney",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "50+",
        "coffee_price": "£2.80"
    },
    {
        "name": "Ace Hotel Shoreditch",
        "map_url": "https://g.page/acehotellondon?share",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipP_NbZH7A1fIQyp5pRm1jOGwzKsDWewaxka6vDt=s0",
        "location": "Shoreditch",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "50+",
        "coffee_price": "£3.00"
    },
    {
        "name": "Goswell Road Coffee",
        "map_url": "https://goo.gl/maps/D9nXNYK3fa1cxwpK8",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipPnOfo7wTICdiAyybF3iFhD3l5aoQjSO-GErma1=s0",
        "location": "Clerkenwell",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "10-20",
        "coffee_price": "£2.10"
    },
    {
        "name": "The Southwark Cathedral Cafe",
        "map_url": "https://goo.gl/maps/LU1imQzBCRLFBxKUA",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipMrdTyRRozGBltwxAseQ4QeuNhbED6meQXlCPsx=s0",
        "location": "London Bridge",
        "has_sockets": True,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": True,
        "seats": "20-30",
        "coffee_price": "£2.30"
    },
    {
        "name": "Trade Commercial Road",
        "map_url": "https://goo.gl/maps/v5tzRBVhPFueYp4x6",
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipNtHqqIc3kwhpjknrVcMdkhmpA77LDYKmpOJlxf=s0",
        "location": "Whitechapel",
        "has_sockets": False,
        "has_toilet": True,
        "has_wifi": True,
        "can_take_calls": False,
        "seats": "20-30",
        "coffee_price": "£2.70"
    }
]

def add_cafes_directly():
    print("Starting direct import of cafes")
    with app.app_context():
        # Check if there are cafes already
        existing_cafes = Cafe.query.count()
        print(f"Found {existing_cafes} existing cafes")
        
        if existing_cafes == 0:
            print("Adding cafes directly to database")
            for cafe_data in CAFE_DATA:
                cafe = Cafe(
                    name=cafe_data["name"],
                    map_url=cafe_data["map_url"],
                    img_url=cafe_data["img_url"],
                    location=cafe_data["location"],
                    has_sockets=cafe_data["has_sockets"],
                    has_toilet=cafe_data["has_toilet"], 
                    has_wifi=cafe_data["has_wifi"],
                    can_take_calls=cafe_data["can_take_calls"],
                    seats=cafe_data["seats"],
                    coffee_price=cafe_data["coffee_price"]
                )
                db.session.add(cafe)
            
            db.session.commit()
            print(f"Successfully added {len(CAFE_DATA)} cafes")
        else:
            print(f"Database already has {existing_cafes} cafes. Skipping import.")

if __name__ == "__main__":
    add_cafes_directly() 