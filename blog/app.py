from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from forms import RegistrationForm, LoginForm
from flask_mail import Mail, Message
import os



app = Flask(__name__)

# Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAI:_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv('EMAIL_USER')
app.config["MAIL_PASSWORD"] = os.getenv('EMAIL_PASS')

mail = Mail(app)
 
# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'Iamsohappyandgreatful' # Needed for forms

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

from routes import *

 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)