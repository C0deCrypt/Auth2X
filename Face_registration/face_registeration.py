import cv2
import face_recognition
from cryptography.fernet import Fernet
import mysql.connector
import os



def generate_key():
    """Generate a new encryption key if not already present."""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load the saved encryption key."""
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_encoding(encoding, key):
    """Encrypt face encoding using Fernet."""
    fernet = Fernet(key)
    encoding_str = ','.join(map(str, encoding))
    return fernet.encrypt(encoding_str.encode())



def save_to_database(username, biometric_type, encrypted_data):
    """Save encrypted biometric data with user info into MySQL."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="41257",
        database="auth2x"
    )
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
    else:
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        user_id = cursor.lastrowid

    # Insert biometric data
    cursor.execute("""
        INSERT INTO biometric_data (user_id, type, data)
        VALUES (%s, %s, %s)
    """, (user_id, biometric_type, encrypted_data))

    conn.commit()
    cursor.close()
    conn.close()



def register_face(username):
    print("=== Face Registration ===")

    cap = cv2.VideoCapture(0)
    print("📷 Press 's' to capture your face.")

    face_encoding = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Face Registration", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb)

            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]
                print("✅ Face captured.")
                break
            else:
                print("❌ No face detected. Please try again.")

    cap.release()
    cv2.destroyAllWindows()

    if face_encoding is not None:
        generate_key()
        key = load_key()
        encrypted_data = encrypt_encoding(face_encoding, key)
        save_to_database(username, "face", encrypted_data)
        print(f"🎉 {username} registered successfully!")
        return True
    else:
        return False



if __name__ == "__main__":
    register_face()

