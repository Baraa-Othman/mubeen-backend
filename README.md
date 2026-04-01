# Mubeen AI Backend 🚀

This is the Python FastAPI backend for the **Mubeen** Flutter app. It acts as a secure proxy to process AI requests using Google Gemini while verifying user authentication via Firebase.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- A **Firebase Project** with Authentication enabled.
- A **Google Gemini API Key**.

### 2. Create a Virtual Environment (Recommended)
Open your terminal in the `mubeen_backend` directory and run:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root of the `mubeen_backend` folder (you can copy `.env.example`) and fill in your credentials:
```env
GEMINI_API_KEY=your_gemini_key_here
FIREBASE_PROJECT_ID=your_firebase_id
```
*Note: Ensure your Firebase service account JSON file is placed in the `app/cert/` folder or root as configured in your `main.py`.*

---

## 🏃‍♂️ How to Run

To start the server in development mode (with auto-reload):
```bash
python -m uvicorn app.main:app --reload
```

The backend will be available at: `http://127.0.0.1:8000`

---

## 🔒 Security & Architecture
- **Auth**: Every request must include a valid Firebase ID Token in the `Authorization: Bearer <TOKEN>` header.
- **Proxy Only**: The backend does NOT perform any database operations. Flutter handles all Firestore reads/writes directly.
- **AI Processing**: All prompts are refined and secured on the backend before being sent to Gemini.
