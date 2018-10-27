import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    users = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = users[0]["cash"]

    portfolios = db.execute("SELECT * FROM portfolio WHERE id = :id", id=session["user_id"])

    total_stocks = 0

    for portfolio in portfolios:
        quote = lookup(portfolio["symbol"])
        portfolio["price"] = usd(quote["price"])
        portfolio["stock"] = usd(int(portfolio["shares"]) * float(quote["price"]))
        total_stocks += (int(portfolio["shares"]) * float(quote["price"]))

    return render_template("index.html", portfolios=portfolios, cash=usd(cash), balance=usd(total_stocks + float(cash)))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))
        # checking if the symbol right
        if not quote:
            return apology("Invalid Symbol")
        try:
            # getting amount of shares from the user
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Input Positive Integer")
        except:
            return apology("Input Positive Integer")

        # looking up for price
        price = quote["price"]
        # the price of the stock
        stock = price * shares
        # cash the user own

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]["cash"]

        # checking if the user has enough money
        if cash < stock:
            return apology("You don't have enough money")
        # storing and updating the information in two tables
        else:
            db.execute("INSERT INTO portfolio (shares, id, symbol, name) VALUES( :shares, :id, :symbol, :name)",
                       shares=shares, id=session['user_id'], symbol=request.form.get("symbol"), name=quote["name"])

            db.execute("INSERT INTO history (symbol, shares, price, id) VALUES( :symbol, :shares, :price, :id)",
                       symbol=quote["symbol"], shares=shares, price=usd(quote["price"]), id=session["user_id"])

            users = db.execute("UPDATE users SET cash = cash - :stock WHERE id = :id",
                               id=session["user_id"], stock=quote["price"] * shares)

        return redirect("/")

        # returns the values to the web pageelse:
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    histories = db.execute("SELECT * from history WHERE id = :id", id=session["user_id"])

    return render_template("history.html", histories=histories)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # lookup the information from yahoo stock thing check helpers.py
        quote = lookup(request.form.get("symbol"))

        # Ensure symbol was submitted
        if not quote:
            return apology("Invalid Symbol")

        # returns the values to the web page
        return render_template("quoted.html", name=quote['name'], symbol=quote['symbol'], price=usd(quote['price']))

    else:
        return render_template("quote.html")


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
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))

        if not result:
            return apology("The user name is already taken.")
        session["user_id"] = result
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        try:
            dic = lookup(request.form.get("symbol"))
            # checking if the symbol right
            if not request.form.get("symbol"):
                return apology("Invalid Symbol")
        except:
            return apology("Invalid Symbol")
        try:
            # getting amount of shares from the user
            shares = int(request.form.get("shares"))
            if not int(request.form.get("shares")) > 0:
                return apology("Input Positive Integer")
        except:
            return apology("Input Positive Integer")
        portfolios = db.execute("SELECT  symbol, SUM(shares) AS sum_shares FROM portfolio WHERE id = :id \
        AND symbol = :symbol GROUP by symbol", id=session["user_id"], symbol=dic["symbol"])
        shares = request.form.get("shares")

        if not int(portfolios[0]["sum_shares"]) > int(shares):
            return apology("You don't own that many shares")
        else:
            db.execute("INSERT INTO history (symbol, shares, price, id) VALUES( :symbol, :shares, :price, :id)",
                       symbol=dic["symbol"], shares=- shares, price=usd(dic["price"]), id=session["user_id"])

            users = db.execute("UPDATE users SET cash = cash + :sell WHERE id = :id",
                               id=session["user_id"], sell=dic["price"] * shares)

        shares_total = portfolios[0]["sum_shares"] - shares

        if shares_total == 0:
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=dic["symbol"])
        else:
            db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol",
                       shares=shares_total, id=session["user_id"], symbol=dic["symbol"])

        return redirect("/")

    else:
        portfolios = db.execute("SELECT  symbol, SUM(shares) AS shares FROM portfolio WHERE id = :id \
        GROUP by symbol", id=session["user_id"])

        for portfolio in portfolios:
            symbol = portfolio["symbol"]

        return render_template("sell.html", portfolios=portfolios)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
