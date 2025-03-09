from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import os
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


# User Model (Stores users)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reset_code = db.Column(db.Integer, nullable=True)
    post = db.relationship('Post', backref="author", lazy=True)
    # is_verified = db.Column(db.Boolean, default=False) # Email verification Status
    verification_code = db.Column(db.Integer, nullable=True) # Stores verification code
    
    # def get_verification_token(self, expires_sec= 1800):
        # serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    
        # return serializer.dumps(self.email, salt="email_verification")
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def generate_verication_code(self):
        self.verification_code= random.randint(100000, 999999) # Generate 6-digit code
        
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    # Post Model (Stores blog posts)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=True, default="default.jpg") 
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    

    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    
