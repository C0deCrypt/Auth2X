import cv2
import face_recognition
from cryptography.fernet import Fernet
import mysql.connector
import numpy as np

# ========== Encryption Key Handling ==========
def load_key():
    """Load the saved encryption key."""
    with open("../Face_registration/secret.key", "rb") as key_file:
        return key_file.read()

def decrypt_encoding(encrypted_data, key):
    """Decrypt the encrypted face encoding."""
    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(encrypted_data.encode())
    encoding_list = list(map(float, decrypted_bytes.decode().split(',')))
    return np.array(encoding_list)

# ========== MySQL Database Interaction ==========

def fetch_face_encodings():
    """Fetch encrypted face encodings from the database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="41257",
        database="auth2x"
    )
    cursor = conn.cursor()

    cursor.execute("""
            SELECT u.username, b.data
            FROM users u
            JOIN biometric_data b ON u.id = b.user_id
            WHERE b.biometric_type = 'face'
        """)

    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# ========== Face Authentication ==========

def authenticate_face():
    print("=== Face Authentication ===")
    key = load_key()
    known_faces = []

    for username, encrypted_data in fetch_face_encodings():
        try:
            encoding = decrypt_encoding(encrypted_data, key)
            known_faces.append((username, encoding))
        except Exception as e:
            print(f"⚠️ Error decrypting data for {username}: {e}")

    cap = cv2.VideoCapture(0)
    print("📷 Press 's' to scan your face for authentication.")

    authenticated = False

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Face Authentication", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb)

            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]

                for username, known_encoding in known_faces:
                    matches = face_recognition.compare_faces([known_encoding], face_encoding)
                    if matches[0]:
                        print(f"✅ Welcome back, {username}!")
                        authenticated = True
                        break
                if not authenticated:
                    print("❌ Face not recognized.")
            else:
                print("❌ No face detected. Try again.")

            break

    cap.release()
    cv2.destroyAllWindows()

# ========== Main ==========

if __name__ == "__main__":
    authenticate_face()
