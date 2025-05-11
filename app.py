import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, CafeForm, ReviewForm
import sqlite3
from dotenv import load_dotenv
from datetime import datetime
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
# Create a .env file with SECRET_KEY=your_secret_key_here for better security
load_dotenv()

app = Flask(__name__)
# If no .env file exists, it will use the default secret key (not recommended for production)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configure the database
if os.environ.get('DATABASE_URL'):
    # For Render PostgreSQL database
    logger.info("Using PostgreSQL database")
    db_url = os.environ.get('DATABASE_URL')
    # Make sure we're using postgresql:// not postgres://
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    # For local SQLite database
    logger.info("Using SQLite database")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe_web.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    reviews = db.relationship('Review', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))
    reviews = db.relationship('Review', backref='cafe', lazy=True)
    likes = db.relationship('Like', backref='cafe', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafe.id'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafe.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import data from old database to new database
def import_data_from_old_db():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if cafes already imported
        if Cafe.query.count() == 0:
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

# Routes
@app.route('/')
def home():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))
        
        # Create new user
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home'))
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    reviews = Review.query.filter_by(cafe_id=cafe_id).order_by(Review.date.desc()).all()
    user_liked = False
    if current_user.is_authenticated:
        like = Like.query.filter_by(user_id=current_user.id, cafe_id=cafe_id).first()
        user_liked = like is not None
    like_count = Like.query.filter_by(cafe_id=cafe_id).count()
    review_form = ReviewForm()
    return render_template('cafe_detail.html', cafe=cafe, reviews=reviews, 
                          user_liked=user_liked, like_count=like_count, form=review_form)

@app.route('/add-cafe', methods=['GET', 'POST'])
@login_required
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash('Cafe added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_cafe.html', form=form)

@app.route('/delete-cafe/<int:cafe_id>', methods=['POST'])
@login_required
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    
    # Delete associated reviews and likes
    Review.query.filter_by(cafe_id=cafe_id).delete()
    Like.query.filter_by(cafe_id=cafe_id).delete()
    
    db.session.delete(cafe)
    db.session.commit()
    flash('Cafe deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/add-review/<int:cafe_id>', methods=['POST'])
@login_required
def add_review(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        new_review = Review(
            text=form.text.data,
            rating=form.rating.data,
            user_id=current_user.id,
            cafe_id=cafe_id
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!', 'success')
    
    return redirect(url_for('cafe_detail', cafe_id=cafe_id))

@app.route('/like/<int:cafe_id>', methods=['POST'])
@login_required
def like_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    like = Like.query.filter_by(user_id=current_user.id, cafe_id=cafe_id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        new_like = Like(user_id=current_user.id, cafe_id=cafe_id)
        db.session.add(new_like)
        db.session.commit()
    
    return redirect(url_for('cafe_detail', cafe_id=cafe_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Only import data when running locally
        if not os.environ.get('DATABASE_URL'):
            import_data_from_old_db()
    app.run(debug=True)
else:
    # This will execute when running under Gunicorn
    # Create tables when starting the application on Render
    with app.app_context():
        logger.info("Creating database tables for production...")
        db.create_all()
        logger.info("Tables created successfully") 