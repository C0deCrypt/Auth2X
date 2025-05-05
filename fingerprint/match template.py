# match_template.py
import os
import sys
import json
import numpy as np
import mysql.connector
from cryptography.fernet import Fernet
from match_utils import preprocess_fingerprint, extract_minutiae, compare_minutiae

IMG_WIDTH = 260
IMG_HEIGHT = 300

FINGERPRINT_DIR = "D:/repo/Auth2X/fingerprint/fingerprints/"
DB_CONFIG_PATH = "D:/repo/Auth2X/fingerprint/config/db_config.json"
SECRET_KEY_PATH = "D:/repo/Auth2X/fingerprint/config/secret.key"

username = sys.argv[1]
live_path = os.path.join(FINGERPRINT_DIR, f"{username}_live.dat")

if not os.path.exists(live_path):
    print("ERROR: Live fingerprint file not found.")
    sys.exit(1)

# Load live fingerprint
with open(live_path, 'rb') as f:
    raw = f.read()
if len(raw) != IMG_WIDTH * IMG_HEIGHT:
    print("ERROR: Invalid fingerprint image size.")
    sys.exit(1)

img = np.frombuffer(raw, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))
skeleton = preprocess_fingerprint(img)
live_minutiae = extract_minutiae(skeleton)

if len(live_minutiae) < 10:
    print("ERROR: Poor fingerprint quality.")
    sys.exit(1)

# Load stored template
with open(DB_CONFIG_PATH, 'r') as f:
    db_config = json.load(f)
with open(SECRET_KEY_PATH, 'rb') as f:
    key = f.read()
fernet = Fernet(key)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor.execute("""
    SELECT data FROM biometric_data
    WHERE biometric_type = 'fingerprint'
    AND user_id = (SELECT id FROM users WHERE username = %s)
""", (username,))
result = cursor.fetchone()
cursor.close()
conn.close()

if not result:
    print("ERROR: No stored fingerprint for user.")
    sys.exit(1)

stored_minutiae = json.loads(fernet.decrypt(result[0]).decode())

# Compare
matches, total1, total2 = compare_minutiae(live_minutiae, stored_minutiae)
ratio = matches / max(len(stored_minutiae), 1)

print(f"[DEBUG] Matches: {matches}, Ratio: {ratio:.3f}")
if ratio > 0.65:
    print("AUTH_SUCCESS")
else:
    print("AUTH_FAIL")
