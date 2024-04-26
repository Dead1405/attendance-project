from datetime import date
import mysql.connector
import pickle

# Establish connection
conn = mysql.connector.connect(
    host="sql6.freesqldatabase.com",
    user="sql6702179",
    password="eN5Tlp8Dky",
    database="sql6702179"
)


def get_today_present(x=0):
    cursor = conn.cursor()
    if x == 0:
        cursor.execute(f"SELECT username FROM attendance WHERE date = '{date.today()}' AND status = 'present'")
    else:
        cursor.execute(f"SELECT username FROM attendance WHERE date = '{date.today()}' AND status = 'absent'")
    students_tuples = cursor.fetchall()
    students = [student[0] for student in students_tuples]
    cursor.close()
    return students

attendance_taken = get_today_present()

def get_face_encodings():
    cursor = conn.cursor()
    cursor.execute("SELECT username, face_encodings FROM students")
    face_encodings = cursor.fetchall()
    cursor.close()
    encodings_dict = {}
    for username, encoding_blob in face_encodings:
        encodings_dict[username] = pickle.loads(encoding_blob)
    return encodings_dict


def mark_attendance(username, status):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (username, date, status) VALUES (%s, %s, %s)",
                   (username, date.today(), status))
    conn.commit()
    cursor.close()


known_face_encodings = get_face_encodings()
known_face_encodings_list = list(known_face_encodings.values())
known_face_names = list(known_face_encodings.keys())


