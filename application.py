import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
app.jinja_env.filters["inr"] = inr

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # get portfilo from database
    portfolio = db.execute(
        "SELECT symbol, name, SUM(shares) as quantity, price, total FROM transactions WHERE person_id = ? GROUP BY symbol", session['user_id'])
    shares = []
    value = 0

    for stock in portfolio:
        if stock["quantity"] == 0:
            continue
        quote = lookup(stock["symbol"])
        price = quote["price"]
        total = price * stock["quantity"]
        stock["price"] = usd(price)
        stock["total"] = usd(total)
        shares.append(stock)
        value += round(total, 2)
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])
    balance = cash[0]["cash"]
    grand_total = value + balance

    return render_template("index.html", shares=shares, balance=usd(balance), value=usd(value), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        quote = lookup(symbol)

        if not symbol:
            return apology("Symbol can't be blank.", 400)
        elif quote == None:
            return apology("Please enter a valid symbol.", 400)
        elif not shares:
            return apology("Missing shares.", 400)
        elif not shares.isdigit() or int(shares) < 0:
            return apology("Shares should not be fractional, negative, and non-numeric.", 400)
        else:
            shares = int(shares)
            name = quote["name"]
            price = quote["price"]
            user = session["user_id"]
            money = db.execute("SELECT cash FROM users WHERE id = :id", id=user)
            cash = money[0]["cash"]
            total = shares * price

            if total > cash:
                return apology("Not enough cash. Can't afford!", 400)
            else:
                balance = cash - total
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                db.execute("INSERT INTO transactions (symbol, person_id, shares, price, transacted, name, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           symbol, user, shares, price, timestamp, name, total)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user)
                flash("Successfully bought!")
                return redirect("/")


@app.route("/history")
@login_required
def history():
    history = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE person_id = :id", id=session['user_id'])
    return render_template("history.html", history=history)


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
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Please provide a valid symbol", 400)
        else:
            name = quote["name"]
            symbol = quote["symbol"]
            price = quote["price"]

            return render_template("quoted.html", name=name, symbol=symbol, price=price)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords and confirmation don't match", 400)
        elif len(request.form.get("password")) < 4 or request.form.get("password").isdigit() or request.form.get("password").islower() or request.form.get("password").isupper() or request.form.get("password").isalpha() or request.form.get("password").isalnum():
            return apology("Password must be at least 4 characters long, with at least one lowercase and  one upper case alphabet, one number and one special character.", 403)

        else:
            if len(db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))) == 0:
                query = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", request.form.get("username"),
                                    generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))
                session["user_id"] = query

                return redirect("/")

            else:
                return apology("Username already exists.", 400)

    else:
        flash("Welcome to CS50 Finance! Please enter username and password to register.")
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stats = db.execute(
        "SELECT symbol, SUM(shares) as quantity FROM transactions where person_id = ? GROUP BY symbol", session['user_id'])
    if request.method == "GET":
        symbols = []
        for row in stats:
            symbols.append(row["symbol"])
        return render_template("sell.html", symbols=symbols)
    else:
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not shares or not symbol:
            return apology("Missing symbol/shares", 400)

        elif quote == None:
            return apology("Please enter a valid symbol.", 400)

        else:

            shares_owned = db.execute(
                "SELECT SUM(shares) as quantity FROM transactions where person_id = ? AND symbol = ? GROUP BY symbol ", session['user_id'], symbol)
            if shares > shares_owned[0]["quantity"]:
                return apology("Not enough shares in your portfolio.", 400)
            price = quote["price"]
            value = round(price * shares, 2)
            money = db.execute("SELECT cash FROM users WHERE id = :id", id=session['user_id'])
            cash = money[0]["cash"]
            cash += value
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session['user_id'])
            db.execute("INSERT INTO transactions (symbol, person_id, shares, price, transacted, name, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       symbol, session['user_id'], -(shares), price, timestamp, quote["price"], value)

            flash("Sold!")
            return redirect("/")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """Let user change the password"""
    if request.method == "GET":
        return render_template("changepw.html")

    if request.method == "POST":
        if not request.form.get("password"):
            return apology("Missing password!", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match!", 400)
        elif len(request.form.get("password")) < 4 or request.form.get("password").isdigit() or request.form.get("password").islower() or request.form.get("password").isupper() or request.form.get("password").isalpha() or request.form.get("password").isalnum():
            return apology("Password must be at least 4 characters long, with at least one lowercase and  one upper case alphabet, one number and one special character.", 403)
        else:
            pwdhash = generate_password_hash(request.form.get("password"))
            db.execute("UPDATE users SET hash = :hash WHERE id=:id", hash=pwdhash, id=session["user_id"])
            flash("Password changed!")
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
