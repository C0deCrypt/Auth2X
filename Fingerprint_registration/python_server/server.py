from flask import Flask, request
from cryptography.fernet import Fernet
import json
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MASLAMAH786",
    database="auth3x"
)
cursor = db.cursor()

app = Flask(__name__)

# Load your encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

@app.route('/fingerprint', methods=['POST'])
def receive_fingerprint():
    try:
        data = request.get_json(force=True)
        user = data.get("user", "Unknown")
        mode = data.get("mode", "unknown")

        print(f"\n🛬 Received from user: {user}, mode: {mode}")
        print("📥 Raw data:", data)

        data_str = json.dumps(data)
        encrypted_data = fernet.encrypt(data_str.encode())
        print("🔒 Encrypted:", encrypted_data)

        if mode == "register":
            query = "INSERT INTO fingerprint_logs (user, encrypted_token) VALUES (%s, %s)"
            cursor.execute(query, (user, encrypted_data.decode()))
            db.commit()
            print("✅ Registered and saved to database.")
            return {"status": "registered"}, 200

        elif mode == "login":
            print("🔎 Login requested — matching not implemented yet.")
            return {"status": "login_request", "message": "Login check pending"}, 200

        else:
            return {"status": "error", "message": "Unknown mode"}, 400

    except Exception as e:
        print("❌ Error:", e)
        return {"status": "error", "message": str(e)}, 400

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    try:
        req_data = request.get_json(force=True)
        token = req_data.get("token")

        if not token:
            return {"status": "error", "message": "No token provided"}, 400

        decrypted = fernet.decrypt(token.encode()).decode()
        print("Decrypted data:", decrypted)

        return {"status": "decrypted", "data": decrypted}, 200

    except Exception as e:
        print("Decryption error:", e)
        return {"status": "error", "message": str(e)}, 400

if __name__ == '__main__':
    print("Flask server running with encryption...")
    app.run(host="0.0.0.0", port=5000)
