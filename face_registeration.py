import cv2
import face_recognition
import sqlite3
from cryptography.fernet import Fernet
import os

# Generate and save encryption key (only once)
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

# Load the saved encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt face encoding using Fernet
def encrypt_encoding(encoding, key):
    fernet = Fernet(key)
    encoding_bytes = ','.join(map(str, encoding)).encode()
    encrypted = fernet.encrypt(encoding_bytes)
    return encrypted

# Save encrypted data to SQLite database
def save_to_database(name, encrypted_encoding):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, encoding BLOB)''')
    c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (name, encrypted_encoding))
    conn.commit()
    conn.close()

# Capture face and register
def register_face():
    name = input("Enter your name: ")

    cap = cv2.VideoCapture(0)
    print("Press 's' to capture your face.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Face Registration", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb)
            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]
                print("Face captured and encoded.")
                break
            else:
                print("No face detected. Try again.")

    cap.release()
    cv2.destroyAllWindows()

    generate_key()
    key = load_key()
    encrypted = encrypt_encoding(face_encoding, key)
    save_to_database(name, encrypted)
    print(f"{name} registered successfully!")

if __name__ == "__main__":
    register_face()
