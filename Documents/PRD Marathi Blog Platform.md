# Product Requirements Document
## Marathi Handwritten Blog Platform

**Version:** 2.1
**Date:** June 2, 2026
**Status:** Draft — M0 Repo Cleanup complete

---

## 1. Overview

### 1.1 Product Summary

A personal web application that allows a single author to photograph handwritten articles in Marathi, have them digitized automatically via OCR, review and edit the result, and publish them to a personal blog. Published posts are available in Marathi by default, with an in-place toggle to view an AI-translated English version.

### 1.2 Problem Statement

Writing in Marathi by hand is natural and expressive, but publishing digitally requires either retyping the full article or using complex tools. There is no simple end-to-end pipeline that takes a handwritten Marathi article from paper to published blog post with minimal friction.

### 1.3 Goals

- Minimize the time between writing on paper and publishing online.
- Achieve high OCR accuracy for Marathi (Devanagari script) handwriting over time.
- Provide a clean, readable blog experience for readers in both Marathi and English.
- Keep the workflow simple enough for a non-technical author to use day-to-day.

### 1.4 Non-Goals (v1.0)

- Multi-user support or contributor accounts.
- Support for languages other than Marathi (planned for future versions).
- Comments, likes, or social features on the blog.
- Mobile app (web-responsive is sufficient for v1.0).
- Offline mode.

---

## 2. What Already Exists

A working proof-of-concept has been built at [github.com/mrudulagem/Handwritten-Blog](https://github.com/mrudulagem/Handwritten-Blog). This validates the most critical technical risk in the project — that Google Cloud Vision API can successfully extract Marathi (Devanagari) handwritten text from a photo.

### 2.1 Existing Files

| File | Description |
|---|---|
| `app.py` | Flask backend. Handles image upload, saves to `static/uploads/`, calls Google Cloud Vision `text_detection`, renders result. Credentials loaded via `python-dotenv`. |
| `templates/index.html` | Minimal upload form — file picker and submit button, no styling |
| `templates/result.html` | Shows uploaded image and extracted Marathi text side by side using Jinja2 |
| `requirements.txt` | Python dependencies: `flask`, `google-cloud-vision`, `werkzeug`, `python-dotenv` |
| `.env` | Local environment variables (not committed). Sets `GOOGLE_APPLICATION_CREDENTIALS` to the key file path. |
| `env.example` | Template for `.env` — safe to commit, shows required variables without values |
| `.gitignore` | Excludes `.env`, `*.json`, `key/`, `static/uploads/`, `__pycache__/`, `.vscode/`, etc. |
| `.vscode/settings.json` | VS Code workspace setting: `python.terminal.useEnvFile: true` to auto-load `.env` in terminal |
| `key/` | Google Cloud service account JSON key (git-ignored, never committed) |

### 2.2 Current Stack

- **Backend:** Python, Flask
- **OCR:** Google Cloud Vision API (`text_detection`)
- **Frontend:** Plain HTML + Jinja2 templates (no framework, no styling)
- **Storage:** Local filesystem (`static/uploads/`)
- **Auth:** None
- **Database:** None

### 2.3 Known Issues to Fix

| # | Issue | Location | Status |
|---|---|---|---|
| 1 | Google Cloud credentials path was hardcoded to a local Windows path | `app.py` | ✅ Fixed — moved to `GOOGLE_APPLICATION_CREDENTIALS` env var, loaded via `python-dotenv` |
| 2 | No `requirements.txt` existed | Repo root | ✅ Fixed — `requirements.txt` created with all dependencies |
| 3 | README is basic and manually written | `README.md` | 🟡 In progress |
| 4 | No `.env` or `.gitignore` | Repo root | ✅ Fixed — both added; `.gitignore` excludes `.env`, `*.json`, `key/`, uploads, and `.vscode/` |

---

## 3. Target Architecture

### 3.1 Recommended Stack

| Layer | Choice | Rationale |
|---|---|---|
| Backend / API | Python + Flask | Already proven, handles OCR pipeline |
| Frontend | React (Vite) | Great for component-driven UI (editor, language toggle, blog feed); good learning opportunity |
| Database | PostgreSQL via Supabase | Managed, free tier, handles auth too |
| File Storage | Supabase Storage | Replaces local filesystem; CDN delivery, persistent |
| OCR | Google Cloud Vision API | Already integrated and validated for Devanagari handwriting |
| Translation | Google Cloud Translation API | Same GCP account as Vision, consistent billing |
| Authentication | Supabase Auth (email/password) | Built-in, minimal setup |
| Hosting | Render (Flask API) + Vercel (React) | Free tiers, straightforward deployment for both |

### 3.2 Architecture Overview

```
[React Frontend — Vercel]
        ↕ REST API calls
[Flask Backend — Render]
        ↕
[Google Cloud Vision]   [Google Cloud Translation]
        ↕
[Supabase — PostgreSQL + Storage + Auth]
```

### 3.3 Data Flow

```
Author uploads photo
        ↓
Flask receives image → saves to Supabase Storage
        ↓
Google Cloud Vision extracts Marathi text
        ↓
React side-by-side editor (image left, editable text right)
        ↓
Author reviews and corrects → saves draft
        ↓
Author publishes → Google Translate generates English version
        ↓
Blog post live in Marathi (reader can toggle to English)
```

---

## 4. Immediate Fixes (Pre-Development Cleanup)

These should be done on the existing repo before new development begins.

### 4.1 Environment Variable for GCP Credentials

**Problem:** `app.py` hardcodes the credentials path:
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\mrudu\Documents\..."
```

**Fix:** Remove the hardcoded line. Instead:
1. Create a `.env` file at the repo root:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/keyfile.json
   ```
2. Load it in `app.py` using `python-dotenv`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   # os.environ now has GOOGLE_APPLICATION_CREDENTIALS automatically
   ```
3. Add `.env` and the credentials JSON file to `.gitignore`.

### 4.2 Create `requirements.txt`

```
flask
google-cloud-vision
werkzeug
python-dotenv
```

### 4.3 Rewrite README

The README should include:
- Project description and motivation
- Architecture diagram (text-based is fine)
- Prerequisites (Python, GCP account, Vision API enabled)
- Setup instructions (clone, virtualenv, install requirements, configure `.env`, run)
- Usage walkthrough (upload image → view extracted text)
- Roadmap / what's coming next
- Tech stack table

---

## 5. Features & Requirements

### 5.1 Authentication

| ID | Requirement | Priority | Status |
|---|---|---|---|
| AUTH-1 | Author can log in with email and password | Must Have | ✅ Done |
| AUTH-2 | Session persists across browser sessions | Must Have | ✅ Done |
| AUTH-3 | Forgot password / reset via email | Must Have | 🔴 Not started |
| AUTH-4 | Only authenticated author can access upload/admin area | Must Have | ✅ Done |
| AUTH-5 | Public blog pages accessible without login | Must Have | 🔴 Not started |

> No self-registration. Single author account seeded at setup time via Supabase dashboard.

---

### 5.2 Image Upload

| ID | Requirement | Priority | Status |
|---|---|---|---|
| UPLOAD-1 | Author can upload a photo of a handwritten article | Must Have | ✅ Done (basic) |
| UPLOAD-2 | Accepted formats: JPEG, PNG, HEIC | Must Have | 🟡 Partial (no format validation yet) |
| UPLOAD-3 | Max file size: 20MB per image | Must Have | 🔴 Not started |
| UPLOAD-4 | Multiple pages can be uploaded for a single article | Must Have | 🔴 Not started |
| UPLOAD-5 | Uploaded images stored and linked to draft post | Must Have | 🟡 Partial (local filesystem only) |
| UPLOAD-6 | Drag-and-drop + file picker UI | Should Have | 🔴 Not started |
| UPLOAD-7 | Author can reorder pages after upload | Should Have | 🔴 Not started |
| UPLOAD-8 | Upload progress indicator | Should Have | 🔴 Not started |

---

### 5.3 OCR / Handwriting Recognition

| ID | Requirement | Priority | Status |
|---|---|---|---|
| OCR-1 | Extract Marathi (Devanagari) text from uploaded image | Must Have | ✅ Done |
| OCR-2 | Multi-page articles processed in order and concatenated | Must Have | 🔴 Not started |
| OCR-3 | OCR runs automatically after upload | Must Have | ✅ Done |
| OCR-4 | OCR processing status indicator (processing / done / failed) | Must Have | 🔴 Not started |
| OCR-5 | If OCR fails, author is notified with retry option | Must Have | 🔴 Not started |
| OCR-6 | OCR result stored alongside original image | Must Have | 🟡 Partial (passed to template, not persisted to DB) |
| OCR-7 | Log OCR confidence scores per page | Should Have | 🔴 Not started |
| OCR-8 | Support mixed Marathi/English text | Nice to Have | 🔴 Not started |

> **OCR API:** Google Cloud Vision `text_detection` is already integrated and validated. No change needed.

---

### 5.4 Side-by-Side Editor

| ID | Requirement | Priority | Status |
|---|---|---|---|
| EDIT-1 | Show uploaded image on the left panel | Must Have | ✅ Done (result.html, unstyled) |
| EDIT-2 | Extracted Marathi text in editable area on the right | Must Have | 🟡 Partial (displayed as `<pre>`, not editable) |
| EDIT-3 | Text area renders Devanagari script correctly | Must Have | 🔴 Not started (no font specified yet) |
| EDIT-4 | Author can freely edit digitized text | Must Have | 🔴 Not started |
| EDIT-5 | Author can add an article title in Marathi | Must Have | 🔴 Not started |
| EDIT-6 | Multi-page navigation for image and text | Must Have | 🔴 Not started |
| EDIT-7 | Auto-save draft every 30 seconds | Must Have | 🔴 Not started |
| EDIT-8 | Manual save draft at any time | Must Have | 🔴 Not started |
| EDIT-9 | Devanagari-compatible font (e.g. Noto Sans Devanagari) | Must Have | 🔴 Not started |
| EDIT-10 | Word count displayed | Should Have | 🔴 Not started |
| EDIT-11 | Zoom on image panel | Should Have | 🔴 Not started |
| EDIT-12 | Keyboard shortcut to save (Ctrl/Cmd + S) | Should Have | 🔴 Not started |

---

### 5.5 Translation

| ID | Requirement | Priority | Status |
|---|---|---|---|
| TRANS-1 | English translation auto-generated on publish | Must Have | 🔴 Not started |
| TRANS-2 | Translation stored in DB alongside Marathi text | Must Have | 🔴 Not started |
| TRANS-3 | Author can preview English translation before publishing | Should Have | 🔴 Not started |
| TRANS-4 | Author can manually edit English translation | Should Have | 🔴 Not started |
| TRANS-5 | Translation regenerates if Marathi text is edited post-publish | Should Have | 🔴 Not started |
| TRANS-6 | Post can be published in Marathi even if translation fails | Must Have | 🔴 Not started |

---

### 5.6 Publishing

| ID | Requirement | Priority | Status |
|---|---|---|---|
| PUB-1 | Author can publish a post from the editor | Must Have | 🔴 Not started |
| PUB-2 | Author can save as draft and return later | Must Have | 🔴 Not started |
| PUB-3 | URL slug generated from transliterated Marathi title | Must Have | 🔴 Not started |
| PUB-4 | Author can unpublish a post | Must Have | 🔴 Not started |
| PUB-5 | Author can delete a draft or published post | Must Have | 🔴 Not started |
| PUB-6 | Published date recorded and shown on post | Must Have | 🔴 Not started |

---

### 5.7 Blog — Reader Experience

| ID | Requirement | Priority | Status |
|---|---|---|---|
| BLOG-1 | Homepage lists all published posts with title and date | Must Have | 🔴 Not started |
| BLOG-2 | Posts ordered by published date, newest first | Must Have | 🔴 Not started |
| BLOG-3 | Post page shows title, date, full body text | Must Have | 🔴 Not started |
| BLOG-4 | Blog defaults to Marathi | Must Have | 🔴 Not started |
| BLOG-5 | Language toggle (Marathi / English) on every post | Must Have | 🔴 Not started |
| BLOG-6 | Toggle swaps title and body in place (no page reload) | Must Have | 🔴 Not started |
| BLOG-7 | Language preference remembered for session | Should Have | 🔴 Not started |
| BLOG-8 | Responsive on mobile and desktop | Must Have | 🔴 Not started |
| BLOG-9 | Devanagari font renders correctly across browsers | Must Have | 🔴 Not started |
| BLOG-10 | SEO-friendly (meta tags, Open Graph) | Should Have | 🔴 Not started |

---

### 5.8 Admin Dashboard

| ID | Requirement | Priority | Status |
|---|---|---|---|
| ADMIN-1 | Dashboard lists all drafts and published posts | Must Have | ✅ Done |
| ADMIN-2 | Shows status (Draft/Published), title, and date | Must Have | ✅ Done |
| ADMIN-3 | Click any post to return to editor | Must Have | 🔴 Not started |
| ADMIN-4 | Indicates which posts have/haven't been translated | Should Have | 🔴 Not started |

---

## 6. Data Models

### Post
```
id              UUID (PK)
title_marathi   TEXT
title_english   TEXT (nullable)
body_marathi    TEXT
body_english    TEXT (nullable)
slug            TEXT (unique)
status          ENUM (draft, published)
published_at    TIMESTAMP (nullable)
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### PostImage
```
id              UUID (PK)
post_id         UUID (FK → Post)
storage_url     TEXT
page_order      INTEGER
ocr_raw_text    TEXT
ocr_confidence  FLOAT (nullable)
created_at      TIMESTAMP
```

---

## 7. Non-Functional Requirements

| Requirement | Target |
|---|---|
| OCR processing time | < 10 seconds per page |
| Translation generation time | < 5 seconds |
| Page load time (blog post) | < 2 seconds |
| Image storage | Supabase free tier (up to 1GB) |
| Security | HTTPS only, credentials via env vars, `.gitignore` enforced |
| Browser support | Chrome, Safari, Firefox — latest 2 versions |

---

## 8. Milestones

| Milestone | Scope | Status |
|---|---|---|
| **M0 — Repo Cleanup** | Fix hardcoded credentials → env var, add `requirements.txt`, rewrite README, add `.gitignore` | ✅ Done (README still in progress) |
| **M1 — Foundation** | Supabase setup, DB schema, auth (login/logout), basic admin dashboard shell | ✅ Done |
| **M2 — React Frontend Scaffold** | Vite + React project setup, Flask API refactored to return JSON, React upload component consuming the API | 🔴 Todo |
| **M3 — OCR Pipeline** | Image upload to Supabase Storage, OCR result persisted to DB, side-by-side editor component | 🔴 Todo |
| **M4 — Publishing** | Publish/unpublish, blog reader view in React, draft management | 🔴 Todo |
| **M5 — Translation** | Auto-translation on publish, language toggle on blog | 🔴 Todo |
| **M6 — Polish** | Noto Sans Devanagari font, SEO, mobile responsiveness, performance | 🔴 Todo |
| **M7 — Accuracy Loop** | Correction logging, OCR confidence tracking, accuracy dashboard | 🔴 Todo |

---

## 9. Future Considerations

- Additional Indian languages (Hindi, Gujarati — Devanagari pipeline largely reusable)
- RSS feed for readers
- Tags / categories
- Full-text search across posts
- Reader comments (Giscus or similar)
- Show original handwritten image on published blog post (authenticity feature)
- Export post as PDF

---

## 10. Open Questions

| # | Question |
|---|---|
| 1 | Should the original handwritten image be visible to readers on the published post? |
| 2 | Custom domain for the blog? (affects Vercel/Render config) |
| 3 | Should the English slug or transliterated Marathi slug be used in the URL? |
| 4 | How should paragraph breaks in handwriting be inferred — blank lines, or AI inference? |
