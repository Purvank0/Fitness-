from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "super_secret_key"


@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

DATA_FOLDER = "data"
MEAL_FILE = os.path.join(DATA_FOLDER, "meals.csv")
USER_FILE = os.path.join(DATA_FOLDER, "users.csv")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def load_meals():
    meals = []
    if os.path.exists(MEAL_FILE):
        with open(MEAL_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["calories"] = int(row["calories"])
                row["protein"] = int(row["protein"])
                row["carbs"] = int(row["carbs"])
                row["fat"] = int(row["fat"])
                meals.append(row)
    return meals

def save_meals(meals):
    with open(MEAL_FILE, "w", newline='', encoding='utf-8') as f:
        fieldnames = [
            "id", "name", "category", "ingredients",
            "calories", "protein", "carbs", "fat",
            "instructions", "timestamp"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for meal in meals:
            writer.writerow(meal)

# ===================== AUTH SYSTEM =====================
def load_users():
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    return users

def save_user(email, password):
    exists = os.path.exists(USER_FILE)
    hashed_password = generate_password_hash(password)

    with open(USER_FILE, "a", newline='', encoding='utf-8') as f:
        fieldnames = ["email", "password"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({"email": email, "password": hashed_password})

def user_exists(email):
    return any(user["email"] == email for user in load_users())

def validate_user(email, password):
    for user in load_users():
        if user["email"] == email:
            return check_password_hash(user["password"], password)
    return False


# ===================== ROUTES =====================
@app.route("/")
def home():
    return redirect(url_for("get_started"))

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

from flask import Flask, render_template, request, redirect, url_for, session, flash

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return render_template("login.html")

        if validate_user(email, password):
            session["user"] = email
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password", "danger")
            return render_template("login.html")
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if user_exists(email):
            flash("User already exists. Please login.", "warning")
            return redirect(url_for("login"))
        save_user(email, password)
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/index")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    meals = load_meals()
    return render_template("index.html", meals=meals)

@app.route("/add", methods=["GET", "POST"])
def add_meal():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        meals = load_meals()
        new_id = max([meal["id"] for meal in meals], default=0) + 1
        new_meal = {
            "id": new_id,
            "name": request.form["name"],
            "category": request.form["category"],
            "ingredients": request.form["ingredients"],
            "calories": int(request.form.get("calories", 0)),
            "protein": int(request.form.get("protein", 0)),
            "carbs": int(request.form.get("carbs", 0)),
            "fat": int(request.form.get("fat", 0)),
            "instructions": request.form.get("instructions", ""),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        meals.append(new_meal)
        save_meals(meals)
        return redirect(url_for("index"))
    return render_template("add_meal.html")

@app.route("/view/<int:meal_id>")
def view_meal(meal_id):
    if "user" not in session:
        return redirect(url_for("login"))
    meals = load_meals()
    meal = next((m for m in meals if m["id"] == meal_id), None)
    if meal:
        return render_template("view_meal.html", meal=meal)
    return redirect(url_for("index"))

@app.route("/edit/<int:meal_id>", methods=["GET", "POST"])
def edit_meal(meal_id):
    if "user" not in session:
        return redirect(url_for("login"))
    meals = load_meals()
    meal = next((m for m in meals if m["id"] == meal_id), None)
    if not meal:
        return redirect(url_for("index"))

    if request.method == "POST":
        meal["name"] = request.form["name"]
        meal["category"] = request.form["category"]
        meal["ingredients"] = request.form["ingredients"]
        meal["calories"] = int(request.form.get("calories", 0))
        meal["protein"] = int(request.form.get("protein", 0))
        meal["carbs"] = int(request.form.get("carbs", 0))
        meal["fat"] = int(request.form.get("fat", 0))
        meal["instructions"] = request.form.get("instructions", "")
        save_meals(meals)
        return redirect(url_for("view_meal", meal_id=meal_id))

    return render_template("edit_meal.html", meal=meal)

@app.route("/delete/<int:meal_id>", methods=["POST"])
def delete_meal(meal_id):
    if "user" not in session:
        return redirect(url_for("login"))
    meals = load_meals()
    meals = [m for m in meals if m["id"] != meal_id]
    save_meals(meals)
    return redirect(url_for("index"))

@app.route("/plan", methods=["GET", "POST"])
def meal_plan():
    if "user" not in session:
        return redirect(url_for("login"))
    meals = load_meals()
    selected_meals = []
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    if request.method == "POST":
        ids = request.form.getlist("meal_ids")
        selected_meals = [m for m in meals if str(m["id"]) in ids]
        for m in selected_meals:
            totals["calories"] += m["calories"]
            totals["protein"] += m["protein"]
            totals["carbs"] += m["carbs"]
            totals["fat"] += m["fat"]

    return render_template("meal_plan.html", meals=meals, selected_meals=selected_meals, totals=totals)

if __name__ == "__main__":
    app.run(debug=True)
