import face_recognition
import cv2
import numpy as np
from playsound import playsound
from datetime import date
import mysql.connector
import pickle

# Establish connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="attendance_records"
)


def remove_attendance(username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance WHERE username = %s AND date = %s AND status = %s",
                   (username, date.today(), "absent"))
    conn.commit()
    cursor.close()
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


video_capture = cv2.VideoCapture(0)

known_face_encodings = get_face_encodings()
known_face_encodings_list = list(known_face_encodings.values())
known_face_names = list(known_face_encodings.keys())
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    if process_this_frame:
        # Find all the faces and face encodings in the frame of video
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        face_names = []

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(list(known_face_encodings.values()), face_encoding, tolerance=0.45)

            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings_list, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                if name in attendance_taken:
                    name = "Attendance taken"
                else:
                    mark_attendance(name, 'present')
                    attendance_taken.append(name)
                    playsound("beep.mp3")
            face_names.append(name)
    process_this_frame = not process_this_frame
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
today_absent = get_today_present(1)
for i in known_face_names:
    if (i not in attendance_taken) and (i not in today_absent):
        mark_attendance(i, "absent")
for i in today_absent:
    if i in attendance_taken:
        remove_attendance(i)
