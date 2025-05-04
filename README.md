# Auth2X: Secure Biometric Authentication System

**Tech Stack:** 
- Python
- C++
- MySQL
- Tkinter
- OpenCV
- SecuGen SDK
- SSIM

---

## 🔐 Overview

**Auth2X** is a dual-mode biometric authentication system that supports:

- **Face recognition** (via OpenCV-based facial encoding)
- **Fingerprint matching** (via SecuGen Hamster Plus and image similarity using SSIM)

It supports encrypted storage of biometric data using **Fernet AES encryption** and integrates with a **Tkinter GUI** for both **registration** and **authentication**.

---

## 🧠 Key Features

- 🔐 **Fingerprint & Face Authentication**
- 🔑 **Encrypted Biometric Data Storage**
- 📸 **Auto-saves debug .png files of fingerprints**
- 🗃️ **User info + biometric data stored in MySQL**
- 🖥️ **C++ Executable for Fingerprint Capture using SecuGen SDK**
- 🧪 **SSIM-based fingerprint comparison with debugging logs**

---

## 🗂️ Folder Structure

```
Auth2X/
├── gui/
│   ├── home\_gui.py
│   ├── login\_gui.py
│   ├── register\_gui.py
│   └── result\_gui.py
├── face\_authentication/
│   └── face\_auth.py
├── Face\_registration/
│   └── face\_registeration.py
├── fingerprint/
│   ├── capture/
│   ├── config/
│   │   ├── config.json
│   │   ├── db\_config.json
│   │   └── secret.key
│   ├── encrypt\_store/
│   │   └── store\_encrypt\_data.py
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
````

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

#### `config.json`

```json
{
  "encrypt_fingerprint": true
}
```

#### `db_config.json`

```json
{
  "host": "localhost",
  "user": "root",
  "password": "yourpassword",
  "database": "auth2x"
}
```

#### `secret.key`

```python
from cryptography.fernet import Fernet
with open("secret.key", "wb") as f:
    f.write(Fernet.generate_key())
```

---

## 🧱 C++ Fingerprint EXE Build

* Use Visual Studio to build `CaptureFingerprint.cpp`
* Link with `sgfplib.lib`
* Place all required DLLs next to the EXE
* Output: `CaptureFingerprint.exe` in `x64/Debug/`

---

## 🔐 How to Run

```bash
python gui/home_gui.py
```

---

## 🔄 Workflow Overview

### 🧍‍♂️ Fingerprint Module

#### ✅ Registration:

* Capture fingerprint via SecuGen SDK
* Store image as `.dat`
* Encrypt (if enabled in `config.json`)
* Save in MySQL `biometric_data` table
* Optionally save `.png` for debugging (`debug_raw_registered.png`)

#### 🔐 Authentication:

* Capture new fingerprint
* Decrypt stored fingerprint
* Resize both to `260x300`
* Compare using **SSIM**
* Match if SSIM > 0.85
* Saves comparison images like:

  * `debug_raw_live.png`
  * `debug_raw_stored.png`

👤 **Fingerprint Contributors:**

* **Ramlah Munir** – [LinkedIn](https://www.linkedin.com/in/ramlah-munir-6b2320344)
* **Talal** – [LinkedIn](https://www.linkedin.com/in/muhammad-talal-1675a0351)

---

### 🧑‍🦱 Face Module

#### ✅ Registration:

* Capture live webcam image using OpenCV
* Detect face using `face_recognition` library
* Extract **128-dimension face encoding**
* Encrypt the encoding with **Fernet**
* Store securely in MySQL

#### 🔐 Authentication:

* Fetch encrypted encoding from DB
* Decrypt using Fernet key
* Compare live webcam face with stored encoding using `compare_faces()`
* Authenticate if match returns True

🖼️ Uses real-time webcam view with prompt to press `s` for scan.

👤 **Face Recognition Contributors:**

* **Ayaan Ahmed Khan** – [LinkedIn](https://www.linkedin.com/in/ayaan-ahmed-khan-448600351)
* **Mohammad Umar Nasir** – [LinkedIn](https://www.linkedin.com/in/mohammad-umar-nasir)

---

## 🧪 Debugging & Logs

* Fingerprint Debug PNGs:

  * `debug_raw_registered.png`
  * `debug_raw_stored.png`
  * `debug_raw_live.png`
* Face module logs errors on decryption or detection failures

---

## ❓ FAQ

**Q:** Low SSIM?
**A:** Re-align finger properly, avoid motion blur.

**Q:** Face not detected?
**A:** Check lighting, background, and camera angle.

---

## 📩 Contact

* Fingerprint: [ramlahmunir786@gmail.com](mailto:ramlahmunir786@gmail.com), [Talal's LinkedIn](https://www.linkedin.com/in/muhammad-talal-1675a0351)
* Face: [Ayaan's LinkedIn](https://www.linkedin.com/in/ayaan-ahmed-khan-448600351), [Umar's LinkedIn](https://www.linkedin.com/in/mohammad-umar-nasir)

---


