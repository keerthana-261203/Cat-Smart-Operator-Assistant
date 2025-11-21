from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_123'  # Needed for flash() to work

client = MongoClient("mongodb://localhost:27017/")
db = client["cat_operator_db"]
tasks_collection = db["tasks"]
bookings_collection = db["bookings"]

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    operator_id = request.form.get("username")
    password = request.form.get("password")

    if not operator_id or not password:
        flash("Please enter both username and password.")
        return redirect(url_for('login'))

    if operator_id == password:
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials. Username and password must match.")
        return redirect(url_for('login'))

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/dashboard.html')
def dashboard():
    today = datetime.now().date()
    all_tasks = list(tasks_collection.find())
    today_tasks = []
    non_today_tasks = []

    for task in all_tasks:
        try:
            task_date = datetime.strptime(task.get("date", ""), "%Y-%m-%d").date()
            if task_date == today:
                today_tasks.append(task)
            else:
                non_today_tasks.append(task)
        except Exception as e:
            print(f"Error parsing task date: {e}")

    return render_template("dashboard.html", today_tasks=today_tasks, all_tasks=non_today_tasks)

@app.route('/training.html')
def training():
    return render_template("training.html")

@app.route('/safety.html')
def safety():
    return render_template("safety.html")

@app.route('/perf.html')
def perf():
    return render_template("perf.html")

@app.route('/pred.html')
def pred():
    return render_template("pred.html")

@app.route('/report.html')
def report():
    return render_template("report.html")

@app.route('/book-instructor', methods=['POST'])
def book_instructor():
    name = request.form.get("name")
    email = request.form.get("email")
    instructor = request.form.get("instructor")
    date = request.form.get("date")

    if name and email and instructor and date:
        booking = {
            "name": name,
            "email": email,
            "instructor": instructor,
            "date": date,
            "timestamp": datetime.now()
        }
        bookings_collection.insert_one(booking)
        print("✅ Booking inserted successfully")
    else:
        print("❌ Missing form data")

    return redirect(url_for('training'))

if __name__ == "__main__":
    app.run(debug=True)