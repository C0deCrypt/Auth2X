import json
import os
import sys
from cryptography.fernet import Fernet
import mysql.connector
from datetime import datetime

FINGERPRINT_DIR = "D:/repo/Auth2X/fingerprint/fingerprints/"
DB_CONFIG_PATH = "D:/repo/Auth2X/fingerprint/config/db_config.json"
SECRET_KEY_PATH = "D:/repo/Auth2X/fingerprint/config/secret.key"
CONFIG_PATH = "D:/repo/Auth2X/fingerprint/config/config.json"

IMG_WIDTH = 260
IMG_HEIGHT = 300

username = sys.argv[1]

# === Load Config ===
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
encrypt_enabled = config.get("encrypt_fingerprint", True)

# === Load fingerprint ===
fp_path = os.path.join(FINGERPRINT_DIR, username + ".dat")
with open(fp_path, 'rb') as f:
    raw_data = f.read()

if len(raw_data) != IMG_WIDTH * IMG_HEIGHT:
    raise ValueError("Invalid fingerprint image size!")

# === Encrypt if flag is enabled ===
if encrypt_enabled:
    with open(SECRET_KEY_PATH, 'rb') as f:
        key = f.read()
    fernet = Fernet(key)
    data_to_store = fernet.encrypt(raw_data)
else:
    print("[DEBUG] Encryption disabled. Storing raw fingerprint.")
    data_to_store = raw_data

# === Load DB Config ===
with open(DB_CONFIG_PATH, 'r') as f:
    db_config = json.load(f)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
result = cursor.fetchone()
if not result:
    raise Exception(f"No user found with username: {username}")
user_id = result[0]

cursor.execute("""
    INSERT INTO biometric_data (user_id, biometric_type, data, created_at)
    VALUES (%s, %s, %s, %s)
""", (user_id, 'fingerprint', data_to_store, datetime.now()))

conn.commit()
cursor.close()
conn.close()
