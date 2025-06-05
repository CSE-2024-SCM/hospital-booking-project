from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hospital"
)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user'] = email
            return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form['name']
        doctor = request.form['doctor']
        date = request.form['date']
        cursor.execute("INSERT INTO appointments (name, doctor, date) VALUES (%s, %s, %s)", (name, doctor, date))
        conn.commit()
        return redirect('/')
    return render_template('appointment.html')

if __name__ == "__main__":
    app.run(debug=True)

