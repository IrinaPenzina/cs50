import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from os.path import join, dirname, realpath


basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///inspire.db")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        username = request.form.get("username")
        if len(username) < 4:
            return apology("Username must be at least 4 characters long")
        if not username.isalnum():
            return apology("Username may only contain letters and numbers")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm the password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("The passwords do not match.")

        # register user
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        if not result:
            return apology("The user name is already taken.")
        session["user_id"] = result
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":

        # storing pictures
        files = request.files.getlist("img")

        if not files:
            return apology("No files")

        # if user does not select file, browser also
        # submit an empty part without filename

        for file in files:
            print(file)
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Joining the base and the requested path
                # img_path=file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                # create the path
                img_path = join('static/images/', filename)
                # apologise if the path exists
                if os.path.exists(img_path):
                    return apology("You have uploaded this image already")
                else:  # save the images
                    file.save(join(dirname(realpath(__file__)), img_path))

                # insert into the database
                db.execute("INSERT INTO images (id, img_path) VALUES (:id, :img_path)", id=session["user_id"],
                           img_path=img_path)
            else:
                return apology("Give me some images!")

        # storing text
        #message = request.form.get("Inspirational text")
        if request.form.get("Inspirational text"):
            if len(request.form.get("Inspirational text")) < 15:
                db.execute("INSERT INTO text (id, message) VALUES(:id, :message)",
                           id=session["user_id"], message=request.form.get("Inspirational text"))
            else:
                return apology("Message has to be less then 15 characters.")
        else:
            return apology("Say something inspiring!")

        # update the user's text
        db.execute("UPDATE text SET message = :message WHERE id = :id",
                   id=session["user_id"], message=request.form.get("Inspirational text"))

        return redirect("/")

    else:
        return render_template('upload.html')


@app.route("/")
@login_required
def index():
    # to show user's uploads
    user_images = db.execute("SELECT img_path FROM images WHERE id = :id", id=session["user_id"])
    user_texts = db.execute("SELECT message FROM text WHERE id = :id", id=session["user_id"])

    someArray = ["/upload"]

    return render_template("index.html", user_images=user_images, user_texts=user_texts)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)