import os
import sys
import mysql.connector
from cryptography.fernet import Fernet
from datetime import datetime
import json

# Load DB config
with open('../config/db_config.json', 'r') as f:
    db_config = json.load(f)

# Load encryption key
with open('../config/secret.key', 'rb') as key_file:
    key = key_file.read()
fernet = Fernet(key)

# Check arguments
if len(sys.argv) != 2:
    print("Usage: python store_encrypted_data.py <username>")
    sys.exit(1)

username = sys.argv[1]
file_path = f"../fingerprints/{username}.dat"

# Check file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    sys.exit(1)

# Read and encrypt fingerprint
with open(file_path, 'rb') as f:
    raw_data = f.read()
encrypted_data = fernet.encrypt(raw_data)

# Store in MySQL
conn = mysql.connector.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database='auth2x'
)
cursor = conn.cursor()

# Find user ID
cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
result = cursor.fetchone()
if not result:
    print(f"User '{username}' not found.")
    sys.exit(1)
user_id = result[0]

# Insert into biometric_data
cursor.execute("""
    INSERT INTO biometric_data (user_id, biometric_type, data, created_at)
    VALUES (%s, %s, %s, %s)
""", (user_id, 'fingerprint', encrypted_data, datetime.now()))
conn.commit()

cursor.close()
conn.close()

print("✅ Fingerprint stored successfully.")
