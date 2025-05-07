import os
import sys
import json
import numpy as np
import mysql.connector
from cryptography.fernet import Fernet
from match_utils import preprocess_fingerprint, extract_minutiae, compare_minutiae

IMG_WIDTH = 260
IMG_HEIGHT = 300

# === [PATH CONFIGURATION] ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # points to Auth2X/
FINGERPRINT_DIR = os.path.join(BASE_DIR, "fingerprint", "fingerprints")
DB_CONFIG_PATH = os.path.join(BASE_DIR, "fingerprint", "config", "db_config.json")
SECRET_KEY_PATH = os.path.join(BASE_DIR, "fingerprint", "config", "secret.key")

# === [GET USERNAME] ===
if len(sys.argv) < 2:
    print("ERROR: Username argument not provided.")
    sys.exit(1)

username = sys.argv[1]
live_path = os.path.join(FINGERPRINT_DIR, f"{username}_live.dat")

print(f"[DEBUG] Looking for live fingerprint at: {live_path}")

try:
    # === [LOAD FINGERPRINT DATA] ===
    if not os.path.exists(live_path):
        print("ERROR: Live fingerprint file not found.")
        sys.exit(1)

    with open(live_path, 'rb') as f:
        raw = f.read()

    print("[DEBUG] Raw fingerprint data size:", len(raw))

    if len(raw) != IMG_WIDTH * IMG_HEIGHT:
        print("ERROR: Invalid fingerprint image size.")
        sys.exit(1)

    img = np.frombuffer(raw, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))
    skeleton = preprocess_fingerprint(img)
    live_minutiae = extract_minutiae(skeleton)

    print("[DEBUG] Extracted", len(live_minutiae), "minutiae from live fingerprint")

    if len(live_minutiae) < 10:
        print("ERROR: Poor fingerprint quality.")
        sys.exit(1)

    # === [LOAD STORED TEMPLATE] ===
    with open(DB_CONFIG_PATH, 'r') as f:
        db_config = json.load(f)
    with open(SECRET_KEY_PATH, 'rb') as f:
        key = f.read()
    fernet = Fernet(key)

    print("[DEBUG] Connecting to MySQL...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data FROM biometric_data
        WHERE type = 'finger'
        AND user_id = (SELECT id FROM users WHERE username = %s)
    """, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        print("ERROR: No stored fingerprint for user.")
        sys.exit(1)

    decrypted = fernet.decrypt(result[0])
    stored_minutiae = json.loads(decrypted.decode())

    print("[DEBUG] Loaded stored minutiae:", len(stored_minutiae))

    # === [COMPARE TEMPLATES] ===
    matches, total1, total2 = compare_minutiae(live_minutiae, stored_minutiae)
    ratio = matches / max(len(stored_minutiae), 1)

    print(f"[DEBUG] Matches: {matches}, Ratio: {ratio:.3f}")
    if ratio > 0.65:
        print("AUTH_SUCCESS")
    else:
        print("AUTH_FAIL")

except Exception as e:
    print("UNEXPECTED ERROR:", str(e))
    sys.exit(1)
