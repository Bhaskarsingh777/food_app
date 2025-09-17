from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # required for session/flash messages

# Database path (SQLite)
DB_NAME = "fooddb.sqlite"

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- SIGNUP ----------
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

    flash("Signup successful! Please login.")
    return redirect(url_for("home"))

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = email
        flash("Login successful!")
    else:
        flash("Invalid email or password.")
    return redirect(url_for("home"))

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.")
    return redirect(url_for("home"))

# ---------- ORDER ----------
@app.route("/order", methods=["POST"])
def order():
    if "user" not in session:
        flash("Please login to place an order.")
        return redirect(url_for("home"))

    item = request.form["item"]
    name = request.form["name"]
    quantity = request.form["quantity"]
    address = request.form["address"]
    phone = request.form["phone"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (item, name, quantity, address, phone) VALUES (?, ?, ?, ?, ?)",
        (item, name, quantity, address, phone)
    )
    conn.commit()
    conn.close()

    flash("Order placed successfully!")
    return redirect(url_for("home"))

# ---------- ADMIN DASHBOARD ----------
@app.route("/admin")
def admin_dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", orders=orders)


# ---------- MAIN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env var
    app.run(host="0.0.0.0", port=port, debug=True)
