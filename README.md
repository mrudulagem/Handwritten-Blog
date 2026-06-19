# Handwritten Blog — Marathi OCR to Blog Platform

A personal web application that converts handwritten Marathi articles into published blog posts. Write by hand, photograph, upload — and the app digitizes your Marathi (Devanagari) text using Google Cloud Vision OCR, lets you review and edit it, and publishes it as a blog post with an optional English translation.

---

## Current Status

**This repo is currently at M1 — Foundation complete (auth, DB schema, admin dashboard).**
The core OCR pipeline is working. Supabase auth (login/logout) and the admin dashboard shell are in place. The React frontend and full blog platform are under active development. See the [Roadmap](#roadmap) below.

---

## How It Works (Current)

```
You upload a photo of your handwritten Marathi article
        ↓
Google Cloud Vision extracts the Devanagari text
        ↓
The app displays the image and extracted text side by side
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| OCR | Google Cloud Vision API |
| Frontend (current) | HTML + Jinja2 |
| Frontend (planned) | React (Vite) |
| Database (planned) | PostgreSQL via Supabase |
| Storage (planned) | Supabase Storage |

---

## Prerequisites

- Python 3.9+
- A [Google Cloud](https://cloud.google.com/) account with the **Vision API** enabled
- A GCP service account with a downloaded JSON credentials file

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/mrudulagem/Handwritten-Blog.git
cd Handwritten-Blog
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in all required values:

```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcp-keyfile.json
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SECRET_KEY=a-long-random-string-for-flask-sessions
```

> ⚠️ Never commit your `.env` file or your credentials JSON. Both are in `.gitignore`.

### 5. Run the app

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Usage

1. Open the app at `http://localhost:5000`
2. Click **Choose File** and select a photo of your handwritten Marathi article
3. Click **Upload**
4. The app displays your uploaded image alongside the extracted Marathi text

---

## Project Structure

```
Handwritten-Blog/
├── app.py                  # Flask backend — routes, auth, OCR pipeline
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables
├── .gitignore
├── CLAUDE.md               # Project context for Claude Code sessions
├── supabase/
│   └── schema.sql          # DB schema — posts and post_images tables
├── static/
│   └── uploads/            # Uploaded images (local, not committed)
└── templates/
    ├── login.html          # Login form (Supabase Auth)
    ├── admin.html          # Admin dashboard — post list
    ├── index.html          # Upload form
    └── result.html         # Side-by-side image + extracted text
```

---

## Roadmap

| Milestone | Description | Status |
|---|---|---|
| M0 — Cleanup | Env vars, requirements.txt, README, .gitignore | ✅ Done |
| M1 — Foundation | Supabase setup, DB schema, auth (login/logout) | 🟡 Partial — AUTH-1, AUTH-4, DB schema done; AUTH-3, AUTH-5 deferred |
| M2 — React Frontend | Vite + React scaffold, Flask refactored to JSON API | 🔴 Todo |
| M3 — OCR Pipeline | Upload to Supabase Storage, persist OCR to DB, editor UI | 🔴 Todo |
| M4 — Publishing | Publish/unpublish, blog reader view, draft management | 🔴 Todo |
| M5 — Translation | Auto English translation, language toggle on blog | 🔴 Todo |
| M6 — Polish | Noto Sans Devanagari, SEO, mobile, performance | 🔴 Todo |
| M7 — Accuracy Loop | Correction logging, OCR confidence tracking | 🔴 Todo |

---

## License

MIT
