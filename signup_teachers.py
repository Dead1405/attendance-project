from flask import Flask, render_template, request
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


# Route for the teacher signup page
@app.route('/signup_teacher', methods=['GET', 'POST'])
def signup_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insert the new teacher into the database
        cursor.execute("INSERT INTO teachers (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        return "Teacher signed up successfully"

    return render_template('teacher_signup.html')


if __name__ == '__main__':
    app.run(debug=True)
