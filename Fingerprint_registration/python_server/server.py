from flask import Flask, request
from cryptography.fernet import Fernet
import json

app = Flask(__name__)

# Load your encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

@app.route('/fingerprint', methods=['POST'])
def receive_fingerprint():
    try:
        data = request.get_json(force=True)
        print("📥 Received data:", data)

        # Convert dict to JSON string before encryption
        data_str = json.dumps(data)
        encrypted_data = fernet.encrypt(data_str.encode())

        # You can print or save this encrypted data
        print("🔒 Encrypted fingerprint data:")
        print(encrypted_data)

        return {"status": "received", "encrypted": encrypted_data.decode()}, 200
    

    except Exception as e:
        print("❌ Error:", e)
        return {"status": "error", "message": str(e)}, 400

if __name__ == '__main__':
    print("🚀 Flask server running with encryption...")
    app.run(host="0.0.0.0", port=5000)