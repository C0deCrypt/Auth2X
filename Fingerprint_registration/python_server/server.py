from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import json
import mysql.connector
import numpy as np
from typing import Dict, Any

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bythebandit@028",
    database="auth2x"
)
cursor = db.cursor()

app = Flask(__name__)

# Load encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

# Configuration
FINGERPRINT_MATCH_THRESHOLD = 0.75  # Similarity threshold (adjust as needed)


@app.route('/fingerprint', methods=['POST'])
def receive_fingerprint():
    try:
        data = request.get_json(force=True)
        user = data.get("user", "Unknown")
        mode = data.get("mode", "unknown")

        print(f"\n🛬 Received from user: {user}, mode: {mode}")
        print("📥 Raw data:", data)

        if mode == "register":
            return register_user(user, data)
        elif mode == "login":
            return login_user(user, data)
        else:
            return {"status": "error", "message": "Unknown mode"}, 400

    except Exception as e:
        print("❌ Error:", e)
        return {"status": "error", "message": str(e)}, 400


def register_user(user: str, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Validate fingerprint data structure
        if 'template' not in data:
            return {"status": "error", "message": "Missing fingerprint template"}, 400

        # Convert to JSON string and encrypt
        data_str = json.dumps(data, sort_keys=True)
        encrypted_data = fernet.encrypt(data_str.encode())

        query = """INSERT INTO fingerprint_logs 
                   (user, encrypted_token) 
                   VALUES (%s, %s)"""
        cursor.execute(query, (user, encrypted_data.decode()))
        db.commit()

        print("✅ Registered and saved to database.")
        return {"status": "success", "message": "Fingerprint registered"}, 200

    except Exception as e:
        print("❌ Registration error:", e)
        db.rollback()
        return {"status": "error", "message": str(e)}, 500


def login_user(user: str, incoming_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Validate incoming data
        if 'template' not in incoming_data:
            return {"status": "error", "message": "Missing fingerprint template"}, 400

        # Fetch last registered encrypted token
        query = """SELECT encrypted_token 
                   FROM fingerprint_logs 
                   WHERE user = %s 
                   ORDER BY id DESC LIMIT 1"""
        cursor.execute(query, (user,))
        result = cursor.fetchone()

        if not result:
            print("❌ No fingerprint registered for user.")
            return {"status": "error", "message": "No fingerprint registered"}, 404

        # Decrypt and parse stored data
        stored_encrypted_token = result[0]
        stored_data = json.loads(fernet.decrypt(stored_encrypted_token.encode()).decode())

        # Compare fingerprint templates
        similarity = compare_templates(
            stored_data['template'],
            incoming_data['template']
        )

        print(f"🔍 Similarity score: {similarity:.2f}")

        if similarity >= FINGERPRINT_MATCH_THRESHOLD:
            print("✅ Fingerprint matched!")
            return {
                "status": "success",
                "message": "Login successful",
                "similarity": float(similarity)
            }, 200
        else:
            print("❌ Fingerprint mismatch.")
            return {
                "status": "error",
                "message": "Fingerprint mismatch",
                "similarity": float(similarity)
            }, 401

    except Exception as e:
        print("❌ Login error:", e)
        return {"status": "error", "message": str(e)}, 500


def compare_templates(template1, template2) -> float:
    """
    Compare two fingerprint templates and return similarity score (0-1)
    """
    try:
        # Convert to numpy arrays for vector operations
        arr1 = np.array(template1)
        arr2 = np.array(template2)

        # Pad shorter array if lengths differ
        if len(arr1) != len(arr2):
            max_len = max(len(arr1), len(arr2))
            arr1 = np.pad(arr1, (0, max_len - len(arr1)), 'constant')
            arr2 = np.pad(arr2, (0, max_len - len(arr2)), 'constant')

        # Calculate cosine similarity
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = np.dot(arr1, arr2) / (norm1 * norm2)
        return max(0.0, min(1.0, similarity))  # Clamp between 0-1

    except Exception as e:
        print("❌ Comparison error:", e)
        return 0.0


@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    try:
        req_data = request.get_json(force=True)
        token = req_data.get("token")

        if not token:
            return {"status": "error", "message": "No token provided"}, 400

        decrypted = fernet.decrypt(token.encode()).decode()
        print("🔓 Decrypted data:", decrypted)

        return {"status": "success", "data": decrypted}, 200

    except Exception as e:
        print("❌ Decryption error:", e)
        return {"status": "error", "message": str(e)}, 400


if __name__ == "__main__":
    print("🚀 Flask server running with encryption...")
    app.run(host="0.0.0.0", port=5000, debug=True)