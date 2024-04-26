from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='C:/Users/surya/Desktop/Python project facial recognition/')

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="attendance_records"
)
cursor = db.cursor()

# Route for the login page
@app.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match in the database
        cursor.execute("SELECT * FROM teachers WHERE username = %s AND password = %s", (username, password))
        teacher = cursor.fetchone()

        if teacher:
            # If credentials match, redirect to the teacher's options page
            return redirect(url_for('teacher_options'))
        else:
            # If credentials don't match, stay on the login page
            return render_template('login_teacher.html')
    return render_template('login_teacher.html')

# Route for the teacher's options page
@app.route('/teacher_options', methods=['GET', 'POST'])
def teacher_options():
    if request.method == 'POST':
        student_username = request.form['student_username']
        
        # Check if the student's username exists in the attendance table
        cursor.execute("SELECT * FROM attendance WHERE username = %s", (student_username,))
        attendance_records = cursor.fetchall()

        return render_template('attendance_records.html', records=attendance_records)
    
    return render_template('teacher_options.html')

# Route to filter attendance records by date
@app.route('/filter_attendance', methods=['POST'])
def filter_attendance():
    if request.method == 'POST':
        date = request.form['date']
        
        # Filter attendance records by the selected date
        cursor.execute("SELECT * FROM attendance WHERE date = %s", (date,))
        attendance_records = cursor.fetchall()

        return render_template('attendance_records.html', records=attendance_records)

if __name__ == '__main__':
    app.run(debug=True)
