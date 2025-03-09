import os
import secrets
from flask_mail import Message
from werkzeug.utils import secure_filename
from app import app, db, login_manager, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request
from model import User, Post
from forms import RegistrationForm, LoginForm, ContactForm
from flask_login import login_user, logout_user, login_required, current_user
import random
# from utils import generate_verification_token


def save_post_image(image):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image.filename)
    image_filename = random_hex + file_ext
    image_path = os.path.join(app.root_path, "static/post_pics", image_filename)
    image.save(image_path)
    return image_filename

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/") # Defines the root of the page
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)
    
@app.route("/about")
def about():
    return render_template("about.html")
    
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Message sent successfully", "success")
        return redirect(url_for("contact"))
        
    return render_template("contact.html", form=form)
 
# def send_verification_email(user):
    # token = user.get_verification_token()
    # verify_url = url_for("verify_email", token=token, _external=True)
    # msg = Message("Verify-YOUr EMail", sender=app.config["MAIL_USERNAME"], recipients=[user.email])
    # msg.body =f"Click the kink to verify your email: {verify_url}"
    # mail.send(msg)
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email is already registered. Please use a different one or log in", "danger")
            return redirect(url_for("register"))
    
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    
        # send_verification_email(user)
        
        # flash("A verification email has been sent. Please check your inbox", "info")
        flash("Account created. You can now login", "success")
        return redirect(url_for("login"))
        
    return render_template('register.html', form=form)
    

@app.route("/login", methods= ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # if not user.is_verified:
                # flash("Please verity your email before logging in", "warning")
                # return redirect(url_for("login"))
                
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check your email and password.", "danger")
    return render_template("login.html", form=form)
               
               

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info" )
    return redirect(url_for('home'))
    
    
    
@app.route("/create_post", methods=["GET","POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        image = request.files['image'] if 'image' in request.files else None
        
        image_filename = save_post_image(image) if image else None
        
        post = Post(title=title, content=content, image_file=image_filename, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("YOUr POSt HAs BEEn CREATEd", "success")
        return redirect(url_for("home"))
        
    return render_template("create_post.html")
    
@app.route("/forgot_password", methods= ["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        
        
        if user:
            verification_code = random.randint(100000, 999999)
            
            user.reset_code = verification_code
            db.session.commit()
            
            msg = Message("Password Reset Code", sender = "macktroy476@gmail.com", recipients = [email])
            msg.body = f"Your password reset code is: {verification_code}"
            mail.send(msg)
            
            flash("A verification code has been sent to your email.", "info")
            return redirect(urlfor("reset_password"))
        else:
            flash("Email not found!", "danger")
            
    return render_template("forgot_password.html")
    
@app.route("/reset_password", methods= ["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        code = request.form["code"]
        new_password = request.form["new_password"]
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.reset_code == int(code):
            
            hashed_password = generate_password_hash(new_password)
            
            user.password = hashed_password
            user.reset_code = None
            db.session.commit()
            
            flash("YOUr PASSWORd HAs BEEn RESEt. YOu CAn NOw LOg In", "success")
            return redirect(url_for("login"))
            
        flash("Invalid code or email", "danger")
        
    return render_template("reset_password.html")
    
# @app.route("/verify_email/<token>")
# def verify_email(token):
    # email = verify_token(token)
    # if not email:
        # flash("The verification link is invalid or has expired.", "danger")
        # return redirect(url_for("register"))
        
    # user = User.query.filter_by(email=email),first()
    # if user:
        # user.is_verified = True
        # db.session(commit)
        # flash("Email verified Successfully? You can Now login.", "success")
        # return redirect(url_for('login'))
        
    # flash("User not found.", "danger")
    # return redirect(url_for("register"))
    
    



# @app.route("/resend_verification")
# def resend_verification():
    # if current_user.is_authenticated:
        # if current_user.email_verified:
            # flash("Your email is already verified.", "info")
            # return redirect(url_for("home"))
        
        # send_verification_email(current_user)
        # flash("A new verification email has been sent.", "info")
        # return redirect(url_for("home"))
    
    # flash("You need to log in first.", "warning")
    # return redirect(url_for("login"))
