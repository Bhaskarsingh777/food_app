from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        name TEXT,
        quantity INTEGER,
        address TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------------- Home ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- Signup ----------------
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        flash("Signup successful! Please login.")
    except sqlite3.IntegrityError:
        flash("Email already exists!")
    finally:
        conn.close()

    return redirect(url_for("home"))

# ---------------- Login ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[3], password):
        session["user"] = user[1]
        flash("Login successful!")
    else:
        flash("Invalid credentials!")
    return redirect(url_for("home"))

# ---------------- Logout ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect(url_for("home"))
# ---------------- Admin Login ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Simple hardcoded admin login (you can improve later)
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin credentials!")

    return render_template("admin_login.html")

# ---------------- Admin Dashboard ----------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", users=users, orders=orders)

# ---------------- Admin Logout ----------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Admin logged out.")
    return redirect(url_for("admin"))


# ----------------- Admin Delete Routes -----------------
@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "admin" not in session:
        return redirect(url_for("admin"))
    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    if "admin" not in session:
        return redirect(url_for("admin"))
    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()
    flash("Order deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))

# ---------------- Order ----------------
@app.route("/order", methods=["POST"])
def order():
    item = request.form["item"]
    name = request.form["name"]
    quantity = request.form["quantity"]
    address = request.form["address"]
    phone = request.form["phone"]

    conn = sqlite3.connect("fooddb.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (item, name, quantity, address, phone) VALUES (?, ?, ?, ?, ?)",
                   (item, name, quantity, address, phone))
    conn.commit()
    conn.close()

    flash(f"Order placed for {quantity} x {item}.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
