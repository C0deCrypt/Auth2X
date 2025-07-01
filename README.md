
# Auth2X: Secure Biometric Authentication System

**Tech Stack:** 
- Python
- C++
- MySQL
- Tkinter
- OpenCV
- SecuGen SDK
- Minutiae-Based Matching

---

## 🔐 Overview

**Auth2X** is a dual-mode biometric authentication system that supports:

- **Face recognition** (via OpenCV-based facial encoding)
- **Fingerprint matching** (via SecuGen Hamster Plus and custom minutiae comparison)

It supports encrypted storage of biometric data using **Fernet AES encryption** and integrates with a **Tkinter GUI** for both **registration** and **authentication**.

---

## 🧠 Key Features

- 🔐 **Fingerprint & Face Authentication**
- 🔑 **Encrypted Biometric Data Storage**
- 🧬 **Minutiae Extraction and Matching (No third-party matcher)**
- 🗃️ **User info + biometric data stored in MySQL**
- 🖥️ **C++ Executable for Fingerprint Capture using SecuGen SDK**
- 🧪 **Match Ratio-based fingerprint comparison with logs**

---

## 📚 Fingerprint Matching Method

This project uses a **minutiae-based fingerprint matching pipeline** that works as follows:

- Captured `.dat` image files (260x300) are loaded as raw binary
- Preprocessing includes binarization, skeletonization, and noise filtering
- Minutiae points (ridge endings & bifurcations) are extracted from the fingerprint skeleton
- Matching is performed by comparing geometrical proximity (Euclidean distance < 10 pixels) and type similarity
- Match ratio is calculated based on overlapping features
- If the match ratio > 0.65, authentication is accepted

All extracted templates are **Fernet-encrypted** before being stored in the database.

---

## 🧰 Libraries Used

- `numpy` – Image array manipulation
- `mysql-connector-python` – Database connection
- `cryptography.fernet` – AES encryption of biometric templates
- `scikit-image` – Image skeletonization and preprocessing
- `tkinter` – GUI interface for user interaction
- `opencv-python` – Face capture and recognition
- `sv-ttk` – Dark theme styling for Tkinter GUI

---

## 🗂️ Folder Structure

```bash
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
│   ├── store_template.py
│   ├── match_template.py
│   ├── match_utils.py
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
* set your fingerprints directory path in sln
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
* Extract minutiae from thinned skeleton
* Encrypt (if enabled in `config.json`)
* Save in MySQL `biometric_data` table

#### 🔐 Authentication:

* Capture new fingerprint
* Extract minutiae
* Fetch and decrypt stored template
* Compare using:
  - Minutiae type match (ending/bifurcation)
  - Euclidean distance < 10 px
* Match if ratio > 0.65
* Terminal logs:  
  `Matches: 24, Ratio: 0.75`

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

* Fingerprint `.dat` storage:
  - `username.dat` and `username_live.dat`
* Logs printed from matcher:
  - `Matches: X, Ratio: 0.YYY`
* Face module logs:
  - Decryption failures
  - Encoding mismatches

---

## ❓ FAQ

**Q:** Low match ratio?  
**A:** Re-align finger, check capture quality, avoid moisture and blur.

**Q:** Face not detected?  
**A:** Use good lighting, keep background simple, position face fully in frame.

---

## 📩 Contact

* Fingerprint: [Ramlah's LinkedIn](https://www.linkedin.com/in/ramlah-munir-6b2320344), [Talal's LinkedIn](https://www.linkedin.com/in/muhammad-talal-1675a0351)  
* Face: [Ayaan's LinkedIn](https://www.linkedin.com/in/ayaan-ahmed-khan-448600351), [Umar's LinkedIn](https://www.linkedin.com/in/mohammad-umar-nasir)
