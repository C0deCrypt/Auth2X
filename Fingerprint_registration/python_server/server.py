import sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/fingerprint', methods=['POST'])
def receive_fingerprint():
    try:
        data = request.get_json(force=True)
        print("🚀 Flask server is running...")
        print("\n✅ Received fingerprint data:", data)

        sys.stdout.flush()
        return {"status": "received"}, 200
    except Exception as e:
        print("❌ Error:", e)
        sys.stdout.flush()
        return {"status": "error", "message": str(e)}, 400

if __name__ == '__main__':

    sys.stdout.flush()
    app.run(host='0.0.0.0', port=5000)