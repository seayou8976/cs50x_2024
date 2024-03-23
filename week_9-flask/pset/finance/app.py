import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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

    id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", id)
    portfolio = db.execute(
        "SELECT symbol, SUM(CASE WHEN transaction_type = 'buy' THEN quantity ELSE -quantity END) AS quantity FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(CASE WHEN transaction_type = 'buy' THEN quantity ELSE -quantity END) <> 0",
        id,
    )
    current_cash = user[0]["cash"]
    current_holding = {}
    total_cash = current_cash

    for p in portfolio:
        stock_price = lookup(p["symbol"])["price"]
        stock_shares = p["quantity"]
        stock_total = stock_price * stock_shares
        current_holding[p["symbol"]] = [stock_shares, stock_price, stock_total]
        total_cash = total_cash + stock_total

    return render_template(
        "index.html",
        current_holding=current_holding,
        current_cash=current_cash,
        total_cash=total_cash,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Assign variables
        symbol = request.form.get("symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be an integer", 400)

        if shares <= 0:
            return apology("cannot buy 0 or negative shares", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = ?", id)
        new_cash = user[0]["cash"] - (float(shares) * quote["price"])

        if new_cash < 0:
            return apology("not enough cash", 400)

        db.execute(
            "INSERT INTO transactions (user_id, symbol, transaction_type, quantity, price) VALUES (?, ?, ?, ?, ?)",
            user[0]["id"],
            symbol,
            "buy",
            shares,
            quote["price"],
        )
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, id)

        flash(f"Purchased {shares} shares of {symbol}")
        return redirect("/")

    return render_template("buy.html")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = ?", id)

        # Verify the user submitted their current password
        username = request.form.get("cur_password")
        if not username:
            return apology("must provide current password", 400)

        # Extra step to validate the user input the correct current password
        if not check_password_hash(user[0]["hash"], request.form.get("cur_password")):
            return apologgy("current password incorrect", 400)

        # Verify the user submitted a new password
        password = request.form.get("new_password")
        if not password:
            return apology("must provide new password", 400)
        # Overwrite the password with the hash for security purposes
        password = generate_password_hash(password)

        # Verify the user confirmed their password
        confirmation = request.form.get("new_confirmation")
        if not confirmation:
            return apology("must confirm password", 400)

        # Verify the new password is not the same as previous
        if check_password_hash(user[0]["hash"], confirmation):
            return apology("new password cannot be the same as previous", 400)

        # Verify both new passwords are the same
        if not check_password_hash(password, confirmation):
            return apology("passwords do not match", 400)

        # Update with the new hashed password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", password, id)

        # Display success and return the user to the login page
        flash("Password Changed")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("changepw.html")

    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    history = db.execute("SELECT * FROM transactions WHERE user_id = ?", id)

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
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Verify the user submitted a username
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        # Ensure usernames are unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("username not available", 400)

        # Verify the user submitted a password
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)
        # Overwrite the password with the hash for security purposes
        password = generate_password_hash(password)

        # Verify the user confirmed their password
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("must confirm password", 400)

        # Verify both passwords are the same
        if not check_password_hash(password, confirmation):
            return apology("passwords do not match", 400)

        # Register the user by inserting their username and hashed password into the db
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?) ", username, password
        )

        # Display success and return the user to the login page
        flash("Sucessfully Registered")
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", id)
    portfolio = db.execute(
        "SELECT symbol, SUM(CASE WHEN transaction_type = 'buy' THEN quantity ELSE -quantity END) AS quantity FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(CASE WHEN transaction_type = 'buy' THEN quantity ELSE -quantity END) <> 0",
        id,
    )

    print(portfolio)

    if request.method == "POST":
        symbol = request.form.get("symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be an integer", 400)

        if shares <= 0:
            return apology("cannot sell 0 or negative shares", 400)

        quote = lookup(symbol)

        new_cash = user[0]["cash"] + (float(shares) * quote["price"])

        if int(shares) > int(portfolio[0]["quantity"]):
            return apology("insufficient shares")

        db.execute(
            "INSERT INTO transactions (user_id, symbol, transaction_type, quantity, price) VALUES (?, ?, ?, ?, ?)",
            id,
            symbol,
            "sell",
            shares,
            quote["price"],
        )
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, id)

        flash(f"Sold {shares} shares of {symbol}")
        return redirect("/")

    return render_template("sell.html", portfolio=portfolio)
