# 🎓 AI Attendance System

An AI-powered attendance system that uses **Face Recognition** and **Voice Recognition** to automatically mark student attendance.

---

## 🚀 Features

- 📸 Face Recognition Attendance
- 🎤 Voice-based Attendance
- 👨‍🎓 Student Dashboard
- 👩‍🏫 Teacher Dashboard
- 📊 Attendance Tracking
- ⚡ Real-time Processing

---

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenCV
- NumPy
- Face Recognition
- Supabase (Database)

---

## 📂 Project Structure

```
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── packages.txt                    # System dependencies for Streamlit Cloud
├── .streamlit/
│   ├── config.toml                 # Streamlit UI/UX config
│   └── secrets.toml.example        # Secrets template
├── src/
│   ├── components/                 # Reusable UI components
│   ├── database/                   # Supabase DB layer
│   ├── pipelines/                  # Face & Voice AI pipelines
│   ├── screens/                    # Teacher & Student screens
│   └── ui/                         # Base layout & styling
└── README.md
```

---

## 🌐 Deploy to Streamlit Cloud

### GitHub URL to Paste
Once pushed to GitHub, paste this exact URL format into Streamlit Cloud:

```
https://github.com/<your-github-username>/<your-repo-name>
```

**Example:**
```
https://github.com/johndoe/snapclass
```

### Steps
1. **Push this repo** to GitHub (e.g., name it `snapclass` or `snap-room`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Paste your GitHub URL, select branch (`main`), and set the main file path to `app.py`.
4. In the app settings, add your **Secrets** (or click the 🔑 key icon in the dashboard):
   ```toml
   SUPABASE_URL = "https://your-project-id.supabase.co"
   SUPABASE_KEY = "your-anon-or-service-role-key"
   ```
5. Click **Deploy**.

> **Note:** `packages.txt` is required because `dlib` and `librosa` need system-level libraries (e.g., `libgl1`, `ffmpeg`) on Linux containers. Streamlit Cloud installs these automatically.

---

## 🔧 Local Development

```bash
# 1. Clone the repo
git clone <repo-url>
cd "snap room"

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add secrets
# Create .streamlit/secrets.toml and fill in your Supabase credentials.
# (See .streamlit/secrets.toml.example for the format.)

# 5. Run the app
streamlit run app.py
```

---

## 🗝️ Secrets Setup

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder values with your actual Supabase credentials.

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-or-service-role-key"
```

**Do not commit** `secrets.toml` to Git — it is already ignored in `.gitignore`.

---

## 📜 License

This project is open-source and available under the MIT License.

