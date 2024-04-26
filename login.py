from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='')

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="attendance_records"
)
cursor = db.cursor()

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match in the database
        cursor.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
        student = cursor.fetchone()

        if student:
            # If credentials match, fetch attendance records
            cursor.execute("SELECT * FROM attendance WHERE username = %s", (username,))
            records = cursor.fetchall()
            return render_template('attendance_records.html', records=records)
        else:
            # If credentials don't match, stay on the login page
            return render_template('login.html')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
