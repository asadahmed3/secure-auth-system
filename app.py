# 🔽 Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy  # for database ORM (object-relational mapping)
from werkzeug.security import generate_password_hash, check_password_hash  # for securely handling passwords
from flask_wtf.csrf import CSRFProtect # for CSRF protection across your app
from dotenv import load_dotenv # Import dotenv to load environment variables from a .env file
import os # For interacting with the operating system (to get environment variables)
from flask_talisman import Talisman

# Load environment variables from the .env file
load_dotenv()

# 🔧 Initialize Flask application
app = Flask(__name__)

# 🔐 Fetch the SECRET_KEY from the environment variables (from .env file)
# If it doesn't exist, use a default 'dev-default-key' (for development purposes only)
app.secret_key = os.getenv('SECRET_KEY', 'dev-default-key')
                                        

Talisman(app)

# 🗃️ Configure database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite file database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disables unnecessary overhead

# 🧠 Initialize the SQLAlchemy database object
db = SQLAlchemy(app)

# Makes Flask verify that token with every POST request
csrf = CSRFProtect(app)

#----------------------------------------------------------------------------------------------#

# Disable debug mode in production
app.config['DEBUG'] = False

# Custom error handler for server errors (500)
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


app.config.update(
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript from accessing cookies
    SESSION_COOKIE_SECURE=False,    # Use only over HTTPS (set to True in production)
    SESSION_COOKIE_SAMESITE='Lax'  # Helps prevent CSRF attacks
)

# 🧍 Define a User model (i.e., table structure in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(100), unique=True, nullable=False)  # Must be unique and not empty
    password = db.Column(db.String(200), nullable=False)  # Stores hashed password

# 🔐 Route: Home page (login form)
@app.route('/')
def home():
    return render_template('login.html')  # Render login.html when visiting the root URL

# 📝 Route: Register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # When user submits the form
        username = request.form['username']
        password = request.form['password']

        # 🔍 Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.')  # Show error
            return redirect(url_for('register'))  # Redirect back to registration form

        # 🔐 Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # 💾 Create a new user and save to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.')  # Confirmation message
        return redirect(url_for('home'))  # Redirect to login page

    return render_template('register.html')  # For GET requests, show the registration form

# 🔐 Route: Login users
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 🔍 Look up the user in the database
    user = User.query.filter_by(username=username).first()

    # ✅ If user exists and password is correct, log them in
    if user and check_password_hash(user.password, password):
        session['user'] = user.username  # Store username in session to remember the user
        return redirect(url_for('dashboard'))  # Go to dashboard

    flash('Invalid username or password.')  # Show login error
    return redirect(url_for('home'))  # Redirect back to login page

# 🔐 Route: Dashboard page (only accessible when logged in)
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('home'))  # Redirect to login if not logged in
    return render_template('dashboard.html', username=session['user'])
   
# 🚪 Route: Log users out
@app.route('/logout', methods=['POST'])  # Uses POST for extra security
def logout():
    session.pop('user', None)  # Remove user from session
    flash('You have been logged out.')  # Optional logout message
    return redirect(url_for('home'))  # Redirect to login page


#----------------------------------------------------------------------------------------------# 

# ▶️ Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)  # Run the app in debug mode (auto-reloads + shows errors)
