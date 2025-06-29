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
            # Always pass user (None if not logged in)
            return render_template("login.html", error=True, user=None)
    # On GET, render login page
    return render_template("login.html", user=session.get('user'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        subjects = [
    request.form.get('subject1'),
    request.form.get('subject2'),
    request.form.get('subject3'),
    request.form.get('subject4'),
    request.form.get('subject5'),
    request.form.get('subject6')
]
        # Pad the subjects list to always have 6 items (fill with None)
        subjects += [None] * (6 - len(subjects))

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO user_details (email, first_name, last_name, password, subject1, subject2, subject3, subject4, subject5, subject6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (email, first_name, last_name, password, *subjects[:6])
        )
        user_id = cur.lastrowid  # Get the new user's id
        conn.commit()
        conn.close()

        session['user'] = {
            'id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'subject1': subjects[0],
            'subject2': subjects[1],
            'subject3': subjects[2],
            'subject4': subjects[3],
            'subject5': subjects[4],
            'subject6': subjects[5]
        }
        return redirect('/home.html')
    return render_template("signup.html")


@app.route('/profile', methods=["GET"])
def profile():
    user = session.get('user')
    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect("/login")
    
@app.route("/stopwatch.html", methods=["GET"])
def stopwatch():
    user = session.get('user')  # Retrieve user data from the session
    if user:
        return render_template('stopwatch.html', user=user)
    else:
        return redirect("/login")  # Redirect to login if no user is logged in

@app.route("/flashcards.html", methods=["GET"])
def flashcards():
    user = session.get('user')  # Retrieve user data from the session
    if user:
        return render_template("flashcards.html", user=user)
    else:
        return redirect("/login")  # Redirect to login if no user is logged in

@app.route("/syllabus.html", methods=["GET"])
def syllabus():
    user = session.get('user')
    if user:
        return render_template("syllabus.html", user=user)
    else:
        return redirect("/login")

@app.route("/flashcardoption.html", methods=["GET"])
def flashcardoption():
    user = session.get('user')  # Retrieve user data from the session
    if user:
        return render_template("flashcardoption.html", user=user)
    else:
        return redirect("/login")  # Redirect to login if no user is logged in

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


def get_db():
    return sqlite3.connect('./database/data_source.db')

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
