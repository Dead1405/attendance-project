from flask import Flask, render_template, request
import mysql.connector
import pickle
import face_recognition

app = Flask(__name__, template_folder='C:/Users/surya/Desktop/Python project facial recognition/')

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="attendance_records"
)
cursor = db.cursor()

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        uploaded_image = request.files['image']

        # Save the uploaded image to a folder
        image_path = 'C:/Users/surya/Desktop/Python project facial recognition/image paths/' + uploaded_image.filename
        uploaded_image.save(image_path)

        # Check if the uploaded image contains any face
        if detect_face(image_path):
            # Generate encoding from the uploaded image
            encoding = generate_encoding(image_path)

            # Insert the new user and encoding into the database
            cursor.execute("INSERT INTO students (username, password, face_encodings, image_path) VALUES (%s, %s, %s, %s)",
                           (username, password, pickle.dumps(encoding), image_path))
            db.commit()

            return "User signed up successfully"
        else:
            return "No face detected in the uploaded image. Please upload an image containing a face."

    return render_template('signup.html')

# Function to detect face in the image
def detect_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    return len(face_locations) > 0

# Function to generate encoding from the image
def generate_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    return encoding

if __name__ == '__main__':
    app.run(debug=True)
