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
        print("\nReceived fingerprint data:", data)

        # Convert dict to JSON string before encryption
        data_str = json.dumps(data)
        encrypted_data = fernet.encrypt(data_str.encode())

        print("Encrypted fingerprint data:")
        print(encrypted_data)

        # Extract user field from JSON
        user = data.get("user", "Unknown")

        # Insert into MySQL
        query = "INSERT INTO fingerprint_logs (user, encrypted_token) VALUES (%s, %s)"
        cursor.execute(query, (user, encrypted_data.decode()))
        db.commit()

        print("Data inserted into MySQL.")

        return {"status": "received", "encrypted": encrypted_data.decode()}, 200

    except Exception as e:
        print("Error:", e)
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
