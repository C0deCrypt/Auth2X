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


# ========== Main ==========

if __name__ == "__main__":
    authenticate_face()
