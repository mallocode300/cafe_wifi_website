# Cafe WiFi Website

A Flask web application for finding and reviewing cafes with WiFi and other amenities.

## Features

- Browse cafes with details on amenities (WiFi, power sockets, toilets, etc.)
- User authentication (register, login, logout)
- Add new cafes to the database
- Like cafes to show your appreciation
- Post reviews with ratings for cafes
- Delete cafes from the database
- Fully responsive design that works on all devices
- Modern, user-friendly interface

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Login for authentication
- Bootstrap for styling
- SQLite for local development
- PostgreSQL for production

## Local Development Setup

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the root directory with the following content:
   ```
   SECRET_KEY=your_secret_key_here
   ```
6. Run the application:
   ```
   python app.py
   ```
7. Open your browser and navigate to `http://127.0.0.1:5000/`

## Deployment on Render

This application is configured for easy deployment on [Render](https://render.com).

### Deployment Steps

1. Push this repository to GitHub
2. Create a Render account at https://render.com
3. In your Render dashboard, click "New" and select "Blueprint"
4. Connect your GitHub account and select this repository
5. Render will automatically detect the `render.yaml` configuration and set up:
   - A web service running your Flask application
   - A PostgreSQL database
   - Environment variables
6. Click "Apply" to start the deployment process
7. Once deployed, your app will be available at `https://cafe-wifi.onrender.com` (or similar)

### Configuration Files

- `render.yaml`: Defines the web service and database
- `build.sh`: Setup script run during deployment
- `init_db.py`: Script to initialize the database
- `wsgi.py`: Entry point for the Gunicorn server

## Recent Updates

- Updated footer with copyright year 2025 and developer attribution
- Improved responsive design for better mobile experience
- Fixed database issues for production deployment on Render

## License

This project is licensed under the MIT License. 