# store_template.py
import os
import sys
import json
import numpy as np
import mysql.connector
from datetime import datetime
from cryptography.fernet import Fernet
from match_utils import preprocess_fingerprint, extract_minutiae

IMG_WIDTH = 260
IMG_HEIGHT = 300
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of the current file
FINGERPRINT_DIR = os.path.join(BASE_DIR, "fingerprints")
DB_CONFIG_PATH = os.path.join(BASE_DIR, "config", "db_config.json")
SECRET_KEY_PATH = os.path.join(BASE_DIR, "config", "secret.key")

username = sys.argv[1]
path = os.path.join(FINGERPRINT_DIR, f"{username}.dat")

with open(path, 'rb') as f:
    raw = f.read()
if len(raw) != IMG_WIDTH * IMG_HEIGHT:
    raise ValueError("Invalid image size.")

img = np.frombuffer(raw, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))
skeleton = preprocess_fingerprint(img)
minutiae = extract_minutiae(skeleton)

# Serialize and encrypt
data_json = json.dumps(minutiae)
with open(SECRET_KEY_PATH, 'rb') as f:
    key = f.read()
fernet = Fernet(key)
encrypted = fernet.encrypt(data_json.encode())

# Save to DB
with open(DB_CONFIG_PATH, 'r') as f:
    db_config = json.load(f)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
result = cursor.fetchone()
if not result:
    raise Exception("User not found")
user_id = result[0]

cursor.execute("""
    INSERT INTO biometric_data (user_id, type, data)
    VALUES (%s, %s, %s)
""", (user_id, 'finger', encrypted))

conn.commit()
cursor.close()
conn.close()

print(f"[INFO] Fingerprint template stored for user: {username}")
