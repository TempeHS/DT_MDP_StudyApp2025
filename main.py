from flask import Flask, redirect, render_template, request, session, Blueprint, jsonify
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import database_manager as dbHandler
import json
import sqlite3

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
    user = session.get('user')  
    if user:
        return render_template('blogs.html', user=user)
    else:
        return redirect("/login")  

@blogpages.route('/decon_eq.html')
def deconstruct():
    user = session.get('user') 
    if user:
        return render_template('decon_eq.html', user=user)
    else:
        return redirect("/login")  
    
@blogpages.route('/cube.html')
def cube():
    user = session.get('user')  
    if user:
        return render_template('cube.html', user=user)
    else:
        return redirect("/login") 

@blogpages.route('/addressverb.html')
def verb():
    user = session.get('user') 
    if user:
        return render_template('addressverb.html', user=user)
    else:
        return redirect("/login") 
    
@blogpages.route('/wheredoistart.html')
def wheredoistart():
    user = session.get('user')  
    if user:
        return render_template('wheredoistart.html', user=user)
    else:
        return redirect("/login") 
    
@blogpages.route('/goals.html')
def goals():
    user = session.get('user')  
    if user:
        return render_template('goals.html', user=user)
    else:
        return redirect("/login") 

@blogpages.route('/examstudyplan.html')
def examstudyplan():
    user = session.get('user')
    if user:
        return render_template('examstudyplan.html', user=user)
    else:
        return redirect("/login") 

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
    user = session.get('user') 
    if user:
        return render_template("privacy.html", user=user)
    else:
        return redirect("/login")  

@app.route("/about.html", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/home.html", methods=["GET"])
def home():
    user = session.get('user')
    if user:
        return render_template("home.html", user=user)
    else:
        return redirect("/login")  

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = dbHandler.check_credentials(email, password)
        if user:
            session['user'] = user
            return redirect("/home.html")
        else:
            return render_template("login.html", error=True, user=None)
    return render_template("login.html", user=session.get('user'))


@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    # Basic validation
    if not all([email, first_name, last_name, password, confirm_password]):
        return render_template("login.html", signup_error="All fields are required.", user=None)
    if password != confirm_password:
        return render_template("login.html", signup_error="Passwords do not match.", user=None)

    # Check if user already exists
    if dbHandler.check_credentials(email, password):
        return render_template("login.html", signup_error="User already exists.", user=None)

    # Insert new user
    dbHandler.insertDetails(email, first_name, last_name, password)

    # Fetch user and log in
    user = dbHandler.check_credentials(email, password)
    session['user'] = user
    return redirect("/home.html")

@app.route('/profile', methods=["GET"])
def profile():
    user = session.get('user')
    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect("/login")
    
@app.route("/stopwatch.html", methods=["GET"])
def stopwatch():
    user = session.get('user')  
    if user:
        return render_template('stopwatch.html', user=user)
    else:
        return redirect("/login") 

@app.route("/bioflashcards.html", methods=["GET"])
def flashcards():
    user = session.get('user')  
    if user:
        return render_template("bioflashcards.html", user=user)
    else:
        return redirect("/login") 

@app.route("/syllabus.html", methods=["GET"])
def syllabus():
    user = session.get('user')
    if user:
        return render_template("syllabus.html", user=user)
    else:
        return redirect("/login")

@app.route("/flashcardoption.html", methods=["GET"])
def flashcardoption():
    user = session.get('user') 
    if user:
        return render_template("flashcardoption.html", user=user)
    else:
        return redirect("/login") 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login.html")

@app.route("/timer.html", methods=["GET"])
def timer():
    user = session.get('user')
    if user:
        return render_template("timer.html", user=user)
    else:
        return redirect("/login")

@app.route("/comingsoon.html", methods=["GET"])
def comingsoon():
    user = session.get('user')
    if user:
        return render_template("comingsoon.html", user=user)
    else:
        return redirect("/login")

@app.route("/samplesyllabus.html", methods=["GET"])
def samplesyllabus():
    user = session.get('user')
    return render_template(
        "samplesyllabus.html",
        user=user
    )


@app.route("/syllabusplaceholder.html", methods=["GET"])
def syllabusplaceholder():
    user = session.get('user')
    return render_template("syllabusplaceholder.html", user=user)


def get_db():
    return sqlite3.connect('./database/data_source.db')

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

@app.route("/privacySL.html", methods=["GET"])
def privacySL():
    user = session.get('user')
    return render_template("privacySL.html", user=user)

@app.route("/biology.html", methods=["GET"])
def biology():
    user = session.get('user')
    return render_template("flashcards/biology.html", user=user)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
