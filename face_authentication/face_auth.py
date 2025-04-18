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

def get_user_encoding(username):
    """Fetch encrypted face encoding for a specific username."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ersatzSQL",
        database="auth2x"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.data
        FROM users u
        JOIN biometric_data b ON u.id = b.user_id
        WHERE u.username = %s AND b.biometric_type = 'face'
    """, (username,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result[0] if result else None

# ========== Face Authentication ==========

def authenticate_face():
    print("=== Face Authentication ===")
    username = input("Enter your username: ").strip()

    key = load_key()
    encrypted_data = get_user_encoding(username)

    if not encrypted_data:
        print("❌ No face data found for this username.")
        return

    try:
        known_encoding = decrypt_encoding(encrypted_data, key)
    except Exception as e:
        print(f"⚠️ Error decrypting data for {username}: {e}")
        return

    cap = cv2.VideoCapture(0)
    print("📷 Press 's' to scan your face for authentication.")

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
                match = face_recognition.compare_faces([known_encoding], face_encoding)[0]

                if match:
                    print(f"✅ Welcome back, {username}!")
                else:
                    print("❌ Face does not match this username.")
            else:
                print("❌ No face detected. Try again.")
            break

    cap.release()
    cv2.destroyAllWindows()

# ========== Main ==========

if __name__ == "__main__":
    authenticate_face()
