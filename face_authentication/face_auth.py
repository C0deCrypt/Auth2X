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


# ========== Face Authentication ==========

def authenticate_face():


# ========== Main ==========

if __name__ == "__main__":
    authenticate_face()
