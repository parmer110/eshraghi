import os
import re
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if session["user_id"]:
        rows2 = db.execute(
            "SELECT symbol, symbol_name, SUM(shares) AS shares, price FROM purchase WHERE person_id = ? GROUP BY symbol", session["user_id"])
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("index.html", rows=rows, rows2=rows2, lookup=lookup, usd=usd)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""

    if request.method == "POST":

        current = request.form.get("current")
        if not current:
            return apology("Please enter current password")

        pas = request.form.get("password")
        if not pas:
            return apology("Please enter password")

        confirm = request.form.get("confirmation")
        if not confirm or pas != confirm:
            return apology("Passwords are not match!")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # Ensure current password is correct
        if not check_password_hash(rows[0]["hash"], current):
            return apology("invalid current password", 403)

        # Check strong password is validated
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(password_pattern, pas):
            return apology("Password should: 1) Has minimum 8 characters in length. 2) At least one uppercase English letter. 3) At least one lowercase English letter. 4) At least one digit. 5) At least one special character.", 400)

        # Register new validated user in database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(pas), session["user_id"])

        # Redirect index
        return redirect("/")

    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("password.html", name=rows[0]["username"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Submit buy
    if request.method == "POST":

        # Initialize
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # validations
        if not lookup(symbol):
            return apology("Symbol does not exist")

        if not (shares.isdigit() and int(shares) > 0):
            return apology("shares should be positive integer")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        shares = int(shares)
        price = lookup(symbol)["price"]
        total = shares * price
        afford = rows[0]["cash"]
        symbol = lookup(symbol)["symbol"]

        if total > afford:
            return apology("Sorry! You are not afford the number of shares at the current price.")

        # Initialize variable
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        d = month + "/" + day + "/" + year
        t = now.strftime("%H:%M:%S")
        symbol = lookup(symbol)["symbol"]
        cash = rows[0]["cash"] - total

        # Update users cash in database
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, rows[0]["id"])

        # Perform for history
        db.execute("INSERT INTO purchase (person_id, name, symbol, symbol_name, price, shares, cash, transactions, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], rows[0]["username"], symbol, lookup(symbol)["name"], price, shares, cash, "buy" if shares > 0 else "sell", d, t)

        # Indexing
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS ind_id ON purchase(id)")
        db.execute("CREATE INDEX IF NOT EXISTS ind_person_id ON purchase(person_id, symbol, shares, price, cash)")

        # Redirect index
        flash("Bought!")
        return redirect("/")

    # If click link to buy
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("buy.html", name=rows[0]["username"])


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM purchase WHERE person_id = ?", session["user_id"])
    rows2 = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("history.html", rows=rows, name=rows2[0]["username"])


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    if request.method == "POST":

        # Initialize
        symbol = request.form.get("symbol")

        if not lookup(symbol):
            return apology("Symbol not exist!", 400)

        symbol = lookup(symbol)["symbol"]
        name_s = lookup(symbol)["name"]
        price = usd(lookup(symbol)["price"])

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        return render_template("quoted.html", symbol=symbol, name_s=name_s, price=price, name=rows[0]["username"])

    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("quote.html", name=rows[0]["username"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Initialize
        user = request.form.get("username")
        pas = request.form.get("password")
        # Ensure password was submitted
        if not pas:
            return apology("missing password", 400)

        # Ensure confirmation was submitted
        elif not (pas == request.form.get("confirmation")):
            return apology("passwords don't match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", user)
        if len(rows) == 1:
            return apology("This username taken before!", 400)

        # Check strong password is validated
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(password_pattern, pas):
            return apology("Password should: 1) Has minimum 8 characters in length. 2) At least one uppercase English letter. 3) At least one lowercase English letter. 4) At least one digit. 5) At least one special character.", 400)

        # Register new validated user in database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, generate_password_hash(pas))
        rows = db.execute("SELECT * FROM users WHERE username = ?", user)
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Submit buy
    if request.method == "POST":

        # Initialization
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        d = month + "/" + day + "/" + year
        t = now.strftime("%H:%M:%S")
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        # Check symbol selected
        if not symbol:
            return apology("Symbol not selected!")

        # Check validate share
        if not shares:
            return apology("must provide share")

        if not (shares.isdigit() and int(shares) > 0):
            return apology("shares should be positive integer")

        symbol = lookup(symbol)["symbol"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        price = lookup(symbol)["price"]
        shares = int(shares)
        total = price * shares
        rows2 = db.execute(
            "SELECT SUM(shares) AS shares, price FROM purchase WHERE person_id = ? AND symbol = ? GROUP BY symbol", session["user_id"], symbol)
        #afford = db.execute("SELECT SUM(price*shares) AS sum FROM purchase WHERE person_id = ? AND symbol = ?", session["user_id"], symbol)
        #afford = afford[0]["sum"]

        if rows2[0]["shares"] * price < total:
            return apology("You have not prerequests for this sale!")

        cash = rows[0]["cash"] + total
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        db.execute("INSERT INTO purchase (person_id, name, symbol, price, shares, cash, transactions, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], rows[0]["username"], symbol, price, -shares, cash, "buy" if shares > 0 else "sell", d, t)

        flash("Sold!")
        return redirect("/")
        # Person dictionary
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    rows2 = db.execute("SELECT DISTINCT(symbol) FROM purchase WHERE person_id = ? AND shares <> ?", session["user_id"], 0)
    return render_template("sell.html", name=rows[0]["username"], rows=rows2)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Cash their account"""

    # Submit cash
    if request.method == "POST":
        paid = request.form.get("cash")
        if not paid:
            return apology("Please input pay")
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"] + int(paid)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, rows[0]["id"])
        return redirect("/")

    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("cash.html", name=rows[0]["username"])
