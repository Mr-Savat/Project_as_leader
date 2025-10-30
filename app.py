from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

APP_SECRET = "change-this-secret"  # change before production

app = Flask(__name__)
app.secret_key = APP_SECRET
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("សូមបញ្ចូល username និង password", "danger")
            return redirect(url_for("register"))

        users = load_users()
        if username in users:
            flash("Username មានរួចហើយ", "danger")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)
        users[username] = {"password": hashed}
        save_users(users)
        flash("ចុះឈ្មោះបានជោគជ័យ។ សូមចូលក្នុងប្រព័ន្ធ", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()
        user = users.get(username)
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            flash("ចូលបានជោគជ័យ!", "success")
            return redirect(url_for("index"))
        else:
            flash("ឈ្មោះឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("បានចាកចេញ", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # ensure users file exists
    if not os.path.exists(USERS_FILE):
        save_users({})
    app.run(debug=True, host="127.0.0.1", port=5000)
