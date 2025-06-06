from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital"
    )

# Home Page
@app.route('/')
def home():
    return render_template("index.html")

# About Page
@app.route('/about')
def about():
    return render_template("about.html")

# Services Page
@app.route('/services')
def services():
    return render_template("services.html")

# Contact Page
@app.route('/contact')
def contact():
    return render_template("contact.html")

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect('/login')
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password_input):
            session['user'] = user['email']
            flash("Login successful!", "success")
            return redirect('/')
        else:
            flash("Invalid email or password!", "danger")

    return render_template("login.html")

# Appointment
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form['name']
        doctor = request.form['doctor']
        date = request.form['date']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO appointments (name, doctor, date) VALUES (%s, %s, %s)", (name, doctor, date))
            conn.commit()
            flash("Appointment booked successfully!", "success")
            return redirect('/')
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("appointment.html")

# Review Page
@app.route('/review')
def review():
    return render_template("review.html")

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

