from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL, NumberRange, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired(), Length(max=250)])
    map_url = StringField('Google Maps URL', validators=[DataRequired(), URL(), Length(max=500)])
    img_url = StringField('Image URL', validators=[DataRequired(), URL(), Length(max=500)])
    location = StringField('Location', validators=[DataRequired(), Length(max=250)])
    has_sockets = BooleanField('Has Power Sockets')
    has_toilet = BooleanField('Has Toilet')
    has_wifi = BooleanField('Has WiFi')
    can_take_calls = BooleanField('Can Take Calls')
    seats = StringField('Number of Seats', validators=[Length(max=250)])
    coffee_price = StringField('Coffee Price', validators=[Length(max=250)])
    submit = SubmitField('Add Cafe')

class ReviewForm(FlaskForm):
    text = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=500)])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Review') 