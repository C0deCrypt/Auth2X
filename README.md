# Auth2X: Secure Biometric Authentication System

**Tech Stack:** Python, C++, MySQL, Tkinter, OpenCV, SecuGen SDK, SSIM

---

## 🔐 Overview

**Auth2X** is a dual-mode biometric authentication system that supports:

- **Face recognition** (via OpenCV-based facial encoding)
- **Fingerprint matching** (via SecuGen Hamster Plus and image similarity using SSIM)

It supports encrypted storage of fingerprint data using **Fernet AES encryption** and is integrated with a Tkinter GUI for both registration and authentication.

---

## 🧠 Key Features

- 🔐 **Fingerprint & Face Authentication**
- 🔑 **Encrypted Fingerprint Storage (Optional)**
- 📸 **Auto-saves debug `.png` files of fingerprints**
- 🗃️ **User info + biometric data stored in MySQL**
- 🖥️ **C++ Executable for Fingerprint Capture using SecuGen SDK**
- 🧪 **Robust SSIM-based fingerprint matching with debug outputs**

---

## 🧱 Folder Structure

```
Auth2X/
├── gui/
│   ├── home_gui.py
│   ├── login_gui.py
│   ├── register_gui.py
│   └── result_gui.py
├── face_authentication/
│   └── face_auth.py
├── Face_registration/
│   └── face_registeration.py
├── fingerprint/
│   ├── capture/
│   ├── config/
│   │   ├── config.json
│   │   ├── db_config.json
│   │   └── secret.key
│   ├── encrypt_store/
│   │   └── store_encrypt_data.py
│   └── fingerprints/
```

---

## 🛠️ Setup Instructions

### 1. ✅ Prerequisites

- Python 3.10+
- MySQL Server
- Visual Studio 2019+
- SecuGen SDK (FDx Pro SDK)
- Python dependencies:
```bash
pip install mysql-connector-python cryptography opencv-python-headless numpy scikit-image sv-ttk pillow
```

---

### 2. 💾 MySQL Schema

```sql
CREATE DATABASE auth2x;
USE auth2x;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE biometric_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    biometric_type ENUM('face', 'fingerprint') NOT NULL,
    data BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

### 3. 🔧 Configuration

- `config.json`
```json
{
  "encrypt_fingerprint": true
}
```

- `db_config.json`
```json
{
  "host": "localhost",
  "user": "root",
  "password": "yourpassword",
  "database": "auth2x"
}
```

- `secret.key`
```python
from cryptography.fernet import Fernet
with open("secret.key", "wb") as f:
    f.write(Fernet.generate_key())
```

---

### 4. 🧱 C++ Fingerprint EXE Build

- Use Visual Studio to build `CaptureFingerprint.cpp`
- Link with `sgfplib.lib`
- Place all required DLLs next to the EXE
- Output: `CaptureFingerprint.exe` in `x64/Debug/`

---

### 5. 🔐 Run the App

```bash
python gui/home_gui.py
```

---

## 🔍 Workflow

### Registration

- Capture fingerprint
- Store image as `.dat`
- Encrypt if enabled
- Store to DB
- store fingerprint as img for testing too(uncomment the raw image line)
### Login

- Capture fingerprint again
- Decrypt stored data
- Reshape both to `(260x300)`
- Compute SSIM
- Match if `SSIM > 0.85`
- store live-fingerprint as img for testing too(uncomment the raw image line)

---

## 🧪 Debugging & Logs

- Fingerprint PNGs:
  - `debug_raw_registered.png`
  - `debug_raw_stored.png`
  - `debug_raw_live.png`

---

## ❓ FAQ

- Low SSIM? Try better alignment.
---

## 📩 Contact

For issues or questions, contact: `ramlahmunir786@gmail.com`

