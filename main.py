from flask import Flask, redirect, render_template, request, session, Blueprint
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import sqlite3
import database_manager as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

# Define the blogpages blueprint
blogpages = Blueprint('blogpages', __name__, template_folder='templates/blogpages')

@blogpages.route('/blogs')
def blogs():
    return render_template('blogs.html')

@blogpages.route('/study')
def study():
    return render_template('study.html')

# Register the blueprint
app.register_blueprint(blogpages, url_prefix='/')

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("login.html")

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("privacy.html")

@app.route("/home.html", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists in user_database and verify password
        user = dbHandler.check_credentials(email, password)
        if user:
            # Store user details in session
            session['user'] = {
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
            # Credentials are correct, redirect to profile or home page
            return redirect("/home.html")
        else:
            # Credentials are incorrect, show error message
            return render_template("login.html", error="Invalid email or password")
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        # Stores user details in user_details database
        dbHandler.insertDetails(email, first_name, last_name, password)

        return redirect("/login")
    return render_template("signup.html")

@app.route("/calendar.html", methods=["GET", "POST"])
def calendar():
    return render_template("calendar.html")

@app.route('/profile', methods=["GET"])
def profile():
    user = session.get('user')
    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect("/login")

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
